# -*- coding: utf-8 -*-
# Copyright 2015 Cyan, Inc.
# Copyright 2017, 2018, 2019 Ciena Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import logging
import struct
import zlib
from binascii import hexlify

from twisted.python.compat import nativeString

from ._util import (
    group_by_topic_and_partition, read_int_string, read_short_ascii,
    read_short_bytes, read_short_text, relative_unpack, write_int_string,
    write_short_ascii, write_short_bytes, write_short_text,
)
from .codec import gzip_decode, gzip_encode, snappy_decode, snappy_encode
from .common import (
    CODEC_GZIP, CODEC_NONE, CODEC_SNAPPY, BrokerMetadata, BufferUnderflowError,
    ChecksumError, ConsumerFetchSizeTooSmall, ConsumerMetadataResponse,
    FetchResponse, InvalidMessageError, Message, OffsetAndMessage,
    OffsetCommitResponse, OffsetFetchResponse, OffsetResponse,
    PartitionMetadata, ProduceResponse, ProtocolError, TopicMetadata,
    UnsupportedCodecError, _HeartbeatResponse, _JoinGroupProtocolMetadata,
    _JoinGroupResponse, _JoinGroupResponseMember, _LeaveGroupResponse,
    _SyncGroupMemberAssignment, _SyncGroupResponse,
)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

_SUPPORTED_CODECS = (CODEC_GZIP, CODEC_NONE, CODEC_SNAPPY)
ATTRIBUTE_CODEC_MASK = 0x03
MAX_BROKERS = 1024

# Default number of msecs the lead-broker will wait for replics to
# ack produce requests before failing the request
DEFAULT_REPLICAS_ACK_TIMEOUT_MSECS = 1000


class _ReprRequest(object):
    r"""
    Wrapper for request `bytes` that gives it a comprehensible repr for use in
    log messages.

    >>> _ReprRequest(b'\0\x02\0\0\0\0\0\xff')
    ListOffsetsRequest0 correlationId=16 (8 bytes)
    """
    __slots__ = ('_request')

    _struct = struct.Struct('>hhi')

    def __init__(self, request):
        assert isinstance(request, bytes), "request must be bytes, not {!r}".format(request)
        self._request = request

    def __str__(self):
        length = len(self._request)
        if length < 8:
            return 'invalid request ({})'.format(hexlify(self._request).decode('ascii'))

        key, version, correlation_id = self._struct.unpack_from(self._request)
        try:
            key_name = KafkaCodec.key_name(key)
        except KeyError:
            return 'request key={}v{} correlationId={} ({:,d} bytes)'.format(
                key, version, correlation_id, length,
            )

        return '{}Request{} correlationId={} ({:,d} bytes)'.format(
            key_name, version, correlation_id, length,
        )

    def __repr__(self):
        return self.__str__()


class KafkaCodec(object):
    """
    Class to encapsulate all of the protocol encoding/decoding.
    This class does not have any state associated with it, it is purely
    for organization.
    """
    # https://kafka.apache.org/protocol.html#protocol_api_keys
    PRODUCE_KEY = 0
    FETCH_KEY = 1
    OFFSET_KEY = 2
    METADATA_KEY = 3
    # Non-user facing control APIs: 4-7
    OFFSET_COMMIT_KEY = 8
    OFFSET_FETCH_KEY = 9
    CONSUMER_METADATA_KEY = 10  # deprecated
    FIND_COORDINATOR_KEY = 10
    JOIN_GROUP_KEY = 11
    HEARTBEAT_KEY = 12
    LEAVE_GROUP_KEY = 13
    SYNC_GROUP_KEY = 14
    DESCRIBE_GROUP_KEY = 15
    LIST_GROUPS_KEY = 16
    SASL_HANDSHAKE_KEY = 17
    API_VERSIONS_KEY = 18
    CREATE_TOPICS_KEY = 19
    DELETE_TOPICS_KEY = 20

    _key_to_name = {
        PRODUCE_KEY: 'Produce',
        FETCH_KEY: 'Fetch',
        OFFSET_KEY: 'ListOffsets',
        METADATA_KEY: 'Metadata',
        OFFSET_COMMIT_KEY: 'OffsetCommit',
        OFFSET_FETCH_KEY: 'OffsetFetch',
        FIND_COORDINATOR_KEY: 'FindCoordinator',
        JOIN_GROUP_KEY: 'JoinGroup',
        HEARTBEAT_KEY: 'Heartbeat',
        LEAVE_GROUP_KEY: 'LeaveGroup',
        SYNC_GROUP_KEY: 'SyncGroup',
        DESCRIBE_GROUP_KEY: 'DescribeGroup',
        LIST_GROUPS_KEY: 'ListGroups',
        SASL_HANDSHAKE_KEY: 'SaslHandshake',
        API_VERSIONS_KEY: 'ApiVersions',
        CREATE_TOPICS_KEY: 'CreateTopics',
        DELETE_TOPICS_KEY: 'DeleteTopics',
    }

    @classmethod
    def key_name(cls, key):
        return cls._key_to_name[key]

    ###################
    #   Private API   #
    ###################

    @classmethod
    def _encode_message_header(cls, client_id, correlation_id, request_key,
                               api_version=0):
        """
        Encode the common request envelope

        :param bytes client_id: Client identifier, a short bytesting.
        :param int correlation_id: 32-bit int
        :param int request_key: Request type identifier, a 16-bit int. See the
            ``*_KEY`` constants above.
        :param int api_version: Version of the request, defaulting to 0.
        """
        return (struct.pack('>hhih',
                            request_key,          # ApiKey
                            api_version,          # ApiVersion
                            correlation_id,       # CorrelationId
                            len(client_id)) +     # ClientId size
                client_id)                        # ClientId

    @classmethod
    def _encode_message_set(cls, messages, offset=None):
        """
        Encode a MessageSet. Unlike other arrays in the protocol,
        MessageSets are not length-prefixed.  Format::

            MessageSet => [Offset MessageSize Message]
              Offset => int64
              MessageSize => int32
        """
        message_set = []
        incr = 1
        if offset is None:
            incr = 0
            offset = 0
        for message in messages:
            encoded_message = KafkaCodec._encode_message(message)
            message_set.append(struct.pack('>qi', offset, len(encoded_message)))
            message_set.append(encoded_message)
            offset += incr
        return b''.join(message_set)

    @classmethod
    def _encode_message(cls, message):
        """
        Encode a single message.

        The magic number of a message is a format version number.  The only
        supported magic number right now is zero.  Format::

            Message => Crc MagicByte Attributes Key Value
              Crc => int32
              MagicByte => int8
              Attributes => int8
              Key => bytes
              Value => bytes
        """
        if message.magic == 0:
            msg = struct.pack('>BB', message.magic, message.attributes)
            msg += write_int_string(message.key)
            msg += write_int_string(message.value)
            crc = zlib.crc32(msg) & 0xffffffff  # Ensure unsigned
            msg = struct.pack('>I', crc) + msg
        else:
            raise ProtocolError("Unexpected magic number: %d" % message.magic)
        return msg

    @classmethod
    def _decode_message_set_iter(cls, data):
        """
        Iteratively decode a MessageSet

        Reads repeated elements of (offset, message), calling decode_message
        to decode a single message. Since compressed messages contain futher
        MessageSets, these two methods have been decoupled so that they may
        recurse easily.
        """
        cur = 0
        read_message = False
        while cur < len(data):
            try:
                ((offset, ), cur) = relative_unpack('>q', data, cur)
                (msg, cur) = read_int_string(data, cur)
                msgIter = KafkaCodec._decode_message(msg, offset)
                for (offset, message) in msgIter:
                    read_message = True
                    yield OffsetAndMessage(offset, message)
            except BufferUnderflowError:
                # NOTE: Not sure this is correct error handling:
                # Is it possible to get a BUE if the message set is somewhere
                # in the middle of the fetch response? If so, we probably have
                # an issue that's not fetch size too small.
                # Aren't we ignoring errors if we fail to unpack data by
                # raising StopIteration()?
                # If _decode_message() raises a ChecksumError, couldn't that
                # also be due to the fetch size being too small?
                if read_message is False:
                    # If we get a partial read of a message, but haven't
                    # yielded anything there's a problem
                    raise ConsumerFetchSizeTooSmall()
                else:
                    return

    @classmethod
    def _decode_message(cls, data, offset):
        """
        Decode a single Message

        The only caller of this method is decode_message_set_iter.
        They are decoupled to support nested messages (compressed MessageSets).
        The offset is actually read from decode_message_set_iter (it is part
        of the MessageSet payload).
        """
        ((crc, magic, att), cur) = relative_unpack('>IBB', data, 0)
        if crc != zlib.crc32(data[4:]) & 0xffffffff:
            raise ChecksumError("Message checksum failed")

        (key, cur) = read_int_string(data, cur)
        (value, cur) = read_int_string(data, cur)

        codec = att & ATTRIBUTE_CODEC_MASK

        if codec == CODEC_NONE:
            yield (offset, Message(magic, att, key, value))

        elif codec == CODEC_GZIP:
            gz = gzip_decode(value)
            for (offset, msg) in KafkaCodec._decode_message_set_iter(gz):
                yield (offset, msg)

        elif codec == CODEC_SNAPPY:
            snp = snappy_decode(value)
            for (offset, msg) in KafkaCodec._decode_message_set_iter(snp):
                yield (offset, msg)

        else:
            raise ProtocolError('Unsupported codec 0b{:b}'.format(codec))

    ##################
    #   Public API   #
    ##################

    @classmethod
    def get_response_correlation_id(cls, data):
        """
        return just the correlationId part of the response

        :param bytes data: bytes to decode
        """
        ((correlation_id,), cur) = relative_unpack('>i', data, 0)
        return correlation_id

    @classmethod
    def encode_produce_request(cls, client_id, correlation_id,
                               payloads=None, acks=1,
                               timeout=DEFAULT_REPLICAS_ACK_TIMEOUT_MSECS):
        """
        Encode some ProduceRequest structs

        :param bytes client_id:
        :param int correlation_id:
        :param list payloads: list of ProduceRequest
        :param int acks:

            How "acky" you want the request to be:

            0: immediate response
            1: written to disk by the leader
            2+: waits for this many number of replicas to sync
            -1: waits for all replicas to be in sync

        :param int timeout:
            Maximum time the server will wait for acks from replicas.  This is
            _not_ a socket timeout.
        """
        if not isinstance(client_id, bytes):
            raise TypeError('client_id={!r} should be bytes'.format(client_id))
        payloads = [] if payloads is None else payloads
        grouped_payloads = group_by_topic_and_partition(payloads)

        message = cls._encode_message_header(client_id, correlation_id,
                                             KafkaCodec.PRODUCE_KEY)

        message += struct.pack('>hii', acks, timeout, len(grouped_payloads))

        for topic, topic_payloads in grouped_payloads.items():
            message += write_short_ascii(topic)

            message += struct.pack('>i', len(topic_payloads))
            for partition, payload in topic_payloads.items():
                msg_set = KafkaCodec._encode_message_set(payload.messages)
                message += struct.pack('>ii', partition, len(msg_set))
                message += msg_set

        return message

    @classmethod
    def decode_produce_response(cls, data):
        """
        Decode bytes to a ProduceResponse

        :param bytes data: bytes to decode
        :returns: iterable of `afkak.common.ProduceResponse`
        """
        ((correlation_id, num_topics), cur) = relative_unpack('>ii', data, 0)

        for _i in range(num_topics):
            topic, cur = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)
            for _i in range(num_partitions):
                ((partition, error, offset), cur) = relative_unpack('>ihq', data, cur)

                yield ProduceResponse(topic, partition, error, offset)

    @classmethod
    def encode_fetch_request(cls, client_id, correlation_id, payloads=None,
                             max_wait_time=100, min_bytes=4096):
        """
        Encodes some FetchRequest structs

        :param bytes client_id:
        :param int correlation_id:
        :param list payloads: list of :class:`FetchRequest`
        :param int max_wait_time: how long to block waiting on min_bytes of data
        :param int min_bytes:
            the minimum number of bytes to accumulate before returning the
            response
        """
        payloads = [] if payloads is None else payloads
        grouped_payloads = group_by_topic_and_partition(payloads)

        message = cls._encode_message_header(client_id, correlation_id,
                                             KafkaCodec.FETCH_KEY)

        assert isinstance(max_wait_time, int)

        # -1 is the replica id
        message += struct.pack('>iiii', -1, max_wait_time, min_bytes,
                               len(grouped_payloads))

        for topic, topic_payloads in grouped_payloads.items():
            message += write_short_ascii(topic)
            message += struct.pack('>i', len(topic_payloads))
            for partition, payload in topic_payloads.items():
                message += struct.pack('>iqi', partition, payload.offset,
                                       payload.max_bytes)

        return message

    @classmethod
    def decode_fetch_response(cls, data):
        """
        Decode bytes to a FetchResponse

        :param bytes data: bytes to decode
        """
        ((correlation_id, num_topics), cur) = relative_unpack('>ii', data, 0)

        for _i in range(num_topics):
            (topic, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)

            for _i in range(num_partitions):
                ((partition, error, highwater_mark_offset), cur) = \
                    relative_unpack('>ihq', data, cur)

                (message_set, cur) = read_int_string(data, cur)

                yield FetchResponse(
                    topic, partition, error,
                    highwater_mark_offset,
                    KafkaCodec._decode_message_set_iter(message_set))

    @classmethod
    def encode_offset_request(cls, client_id, correlation_id, payloads=None):
        payloads = [] if payloads is None else payloads
        grouped_payloads = group_by_topic_and_partition(payloads)

        message = cls._encode_message_header(client_id, correlation_id,
                                             KafkaCodec.OFFSET_KEY)

        # -1 is the replica id
        message += struct.pack('>ii', -1, len(grouped_payloads))

        for topic, topic_payloads in grouped_payloads.items():
            message += write_short_ascii(topic)
            message += struct.pack('>i', len(topic_payloads))

            for partition, payload in topic_payloads.items():
                message += struct.pack('>iqi', partition, payload.time,
                                       payload.max_offsets)

        return message

    @classmethod
    def decode_offset_response(cls, data):
        """
        Decode bytes to an :class:`OffsetResponse`

        :param bytes data: bytes to decode
        """
        ((correlation_id, num_topics), cur) = relative_unpack('>ii', data, 0)

        for _i in range(num_topics):
            (topic, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)

            for _i in range(num_partitions):
                ((partition, error, num_offsets), cur) = \
                    relative_unpack('>ihi', data, cur)

                offsets = []
                for _i in range(num_offsets):
                    ((offset,), cur) = relative_unpack('>q', data, cur)
                    offsets.append(offset)

                yield OffsetResponse(topic, partition, error, tuple(offsets))

    @classmethod
    def encode_metadata_request(cls, client_id, correlation_id, topics=None):
        """
        Encode a MetadataRequest

        :param bytes client_id: string
        :param int correlation_id: int
        :param list topics: list of text
        """
        topics = [] if topics is None else topics
        message = [
            cls._encode_message_header(client_id, correlation_id,
                                       KafkaCodec.METADATA_KEY),
            struct.pack('>i', len(topics)),
        ]
        for topic in topics:
            message.append(write_short_ascii(topic))
        return b''.join(message)

    @classmethod
    def decode_metadata_response(cls, data):
        """
        Decode bytes to a MetadataResponse

        :param bytes data: bytes to decode
        """
        ((correlation_id, numbrokers), cur) = relative_unpack('>ii', data, 0)

        # In testing, I saw this routine swap my machine to death when
        # passed bad data. So, some checks are in order...
        if numbrokers > MAX_BROKERS:
            raise InvalidMessageError(
                "Brokers:{} exceeds max:{}".format(numbrokers, MAX_BROKERS))

        # Broker info
        brokers = {}
        for _i in range(numbrokers):
            ((nodeId, ), cur) = relative_unpack('>i', data, cur)
            (host, cur) = read_short_ascii(data, cur)
            ((port,), cur) = relative_unpack('>i', data, cur)
            brokers[nodeId] = BrokerMetadata(nodeId, nativeString(host), port)

        # Topic info
        ((num_topics,), cur) = relative_unpack('>i', data, cur)
        topic_metadata = {}

        for _i in range(num_topics):
            ((topic_error,), cur) = relative_unpack('>h', data, cur)
            (topic_name, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)
            partition_metadata = {}

            for _j in range(num_partitions):
                ((partition_error_code, partition, leader, numReplicas),
                 cur) = relative_unpack('>hiii', data, cur)

                (replicas, cur) = relative_unpack(
                    '>%di' % numReplicas, data, cur)

                ((num_isr,), cur) = relative_unpack('>i', data, cur)
                (isr, cur) = relative_unpack('>%di' % num_isr, data, cur)

                partition_metadata[partition] = \
                    PartitionMetadata(
                        topic_name, partition, partition_error_code, leader,
                        replicas, isr)

            topic_metadata[topic_name] = TopicMetadata(
                topic_name, topic_error, partition_metadata)

        return brokers, topic_metadata

    @classmethod
    def encode_consumermetadata_request(cls, client_id, correlation_id,
                                        consumer_group):
        """
        Encode a ConsumerMetadataRequest

        :param bytes client_id: string
        :param int correlation_id: int
        :param str consumer_group: string
        """
        message = cls._encode_message_header(client_id, correlation_id,
                                             KafkaCodec.CONSUMER_METADATA_KEY)
        message += write_short_ascii(consumer_group)
        return message

    @classmethod
    def decode_consumermetadata_response(cls, data):
        """
        Decode bytes to a ConsumerMetadataResponse

        :param bytes data: bytes to decode
        """
        (correlation_id, error_code, node_id), cur = \
            relative_unpack('>ihi', data, 0)
        host, cur = read_short_ascii(data, cur)
        (port,), cur = relative_unpack('>i', data, cur)

        return ConsumerMetadataResponse(
            error_code, node_id, nativeString(host), port)

    @classmethod
    def encode_offset_commit_request(cls, client_id, correlation_id,
                                     group, group_generation_id, consumer_id,
                                     payloads):
        """
        Encode some OffsetCommitRequest structs (v1)

        :param bytes client_id: string
        :param int correlation_id: int
        :param str group: the consumer group to which you are committing offsets
        :param int group_generation_id: int32, generation ID of the group
        :param str consumer_id: string, Identifier for the consumer
        :param list payloads: list of :class:`OffsetCommitRequest`
        """
        assert consumer_id is not None
        grouped_payloads = group_by_topic_and_partition(payloads)

        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.OFFSET_COMMIT_KEY,
            api_version=1,
        )

        message += write_short_ascii(group)
        message += struct.pack('>i', group_generation_id)
        message += write_short_ascii(consumer_id)
        message += struct.pack('>i', len(grouped_payloads))

        for topic, topic_payloads in grouped_payloads.items():
            message += write_short_ascii(topic)
            message += struct.pack('>i', len(topic_payloads))

            for partition, payload in topic_payloads.items():
                message += struct.pack('>iqq', partition, payload.offset,
                                       payload.timestamp)
                message += write_short_bytes(payload.metadata)

        return message

    @classmethod
    def decode_offset_commit_response(cls, data):
        """
        Decode bytes to an OffsetCommitResponse

        :param bytes data: bytes to decode
        """
        ((correlation_id,), cur) = relative_unpack('>i', data, 0)
        ((num_topics,), cur) = relative_unpack('>i', data, cur)

        for _i in range(num_topics):
            (topic, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)

            for _i in range(num_partitions):
                ((partition, error), cur) = relative_unpack('>ih', data, cur)
                yield OffsetCommitResponse(topic, partition, error)

    @classmethod
    def encode_offset_fetch_request(cls, client_id, correlation_id,
                                    group, payloads):
        """
        Encode some OffsetFetchRequest structs

        :param bytes client_id: string
        :param int correlation_id: int
        :param bytes group: string, the consumer group you are fetching offsets for
        :param list payloads: list of :class:`OffsetFetchRequest`
        """
        grouped_payloads = group_by_topic_and_partition(payloads)
        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.OFFSET_FETCH_KEY,
            api_version=1)

        message += write_short_ascii(group)
        message += struct.pack('>i', len(grouped_payloads))

        for topic, topic_payloads in grouped_payloads.items():
            message += write_short_ascii(topic)
            message += struct.pack('>i', len(topic_payloads))

            for partition in topic_payloads:
                message += struct.pack('>i', partition)

        return message

    @classmethod
    def decode_offset_fetch_response(cls, data):
        """
        Decode bytes to an OffsetFetchResponse

        :param bytes data: bytes to decode
        """

        ((correlation_id,), cur) = relative_unpack('>i', data, 0)
        ((num_topics,), cur) = relative_unpack('>i', data, cur)

        for _i in range(num_topics):
            (topic, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)

            for _i in range(num_partitions):
                ((partition, offset), cur) = relative_unpack('>iq', data, cur)
                (metadata, cur) = read_short_bytes(data, cur)
                ((error,), cur) = relative_unpack('>h', data, cur)

                yield OffsetFetchResponse(topic, partition, offset,
                                          metadata, error)

    @classmethod
    def encode_join_group_request(cls, client_id, correlation_id,
                                  payload):
        """
        Encode a JoinGroupRequest

        :param bytes client_id: string
        :param int correlation_id: int
        :param :class:`JoinGroupRequest` payload: payload
        """
        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.JOIN_GROUP_KEY,
            api_version=0)

        message += write_short_text(payload.group)
        message += struct.pack('>i', payload.session_timeout)
        message += write_short_text(payload.member_id)
        message += write_short_text(payload.protocol_type)

        message += struct.pack('>i', len(payload.group_protocols))
        for group_protocol in payload.group_protocols:
            message += write_short_ascii(group_protocol.protocol_name)
            message += write_int_string(group_protocol.protocol_metadata)

        return message

    @classmethod
    def encode_join_group_protocol_metadata(cls, version, subscriptions, user_data):
        message = struct.pack('>hi', version, len(subscriptions))
        for subscription in subscriptions:
            message += write_short_text(subscription)
        message += write_int_string(user_data)
        return message

    @classmethod
    def decode_join_group_protocol_metadata(cls, data):
        """
        Decode bytes to a JoinGroupProtocolMetadata

        :param bytes data: bytes to decode
        """
        ((version, num_subscriptions), cur) = relative_unpack('>hi', data, 0)
        subscriptions = []
        for _i in range(num_subscriptions):
            (subscription, cur) = read_short_text(data, cur)
            subscriptions.append(subscription)
        (user_data, cur) = read_int_string(data, cur)
        return _JoinGroupProtocolMetadata(version, subscriptions, user_data)

    @classmethod
    def decode_join_group_response(cls, data):
        """
        Decode bytes to a JoinGroupResponse

        :param bytes data: bytes to decode
        """

        ((correlation_id, error, generation_id), cur) = relative_unpack('>ihi', data, 0)
        (group_protocol, cur) = read_short_text(data, cur)
        (leader_id, cur) = read_short_text(data, cur)
        (member_id, cur) = read_short_text(data, cur)
        ((num_members,), cur) = relative_unpack('>i', data, cur)

        members = []
        for _i in range(num_members):
            (response_member_id, cur) = read_short_text(data, cur)
            (response_member_data, cur) = read_int_string(data, cur)
            members.append(_JoinGroupResponseMember(response_member_id, response_member_data))
        return _JoinGroupResponse(error, generation_id, group_protocol,
                                  leader_id, member_id, members)

    @classmethod
    def encode_leave_group_request(cls, client_id, correlation_id, payload):
        """
        Encode a LeaveGroupRequest
        :param bytes client_id: string
        :param int correlation_id: int
        :param :class:`LeaveGroupRequest` payload: payload
        """
        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.LEAVE_GROUP_KEY,
            api_version=0)

        message += write_short_text(payload.group)
        message += write_short_text(payload.member_id)
        return message

    @classmethod
    def decode_leave_group_response(cls, data):
        """
        Decode bytes to a LeaveGroupResponse

        :param bytes data: bytes to decode
        """
        ((correlation_id, error), cur) = relative_unpack('>ih', data, 0)
        return _LeaveGroupResponse(error)

    @classmethod
    def encode_heartbeat_request(cls, client_id, correlation_id, payload):
        """
        Encode a HeartbeatRequest

        :param bytes client_id: string
        :param int correlation_id: int
        :param :class:`_HeartbeatRequest` payload: payload
        """
        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.HEARTBEAT_KEY,
            api_version=0)

        message += write_short_text(payload.group)
        message += struct.pack('>i', payload.generation_id)
        message += write_short_text(payload.member_id)
        return message

    @classmethod
    def decode_heartbeat_response(cls, data):
        """
        Decode bytes to a `_HeartbeatResponse`

        :param bytes data: bytes to decode
        """
        ((correlation_id, error), cur) = relative_unpack('>ih', data, 0)
        return _HeartbeatResponse(error)

    @classmethod
    def encode_sync_group_request(cls, client_id, correlation_id, payload):
        """
        Encode a SyncGroupRequest

        :param bytes client_id: string
        :param int correlation_id: int
        :param payload: :class:`_SyncGroupRequest`
        """
        message = cls._encode_message_header(
            client_id, correlation_id, KafkaCodec.SYNC_GROUP_KEY,
            api_version=0)

        message += write_short_text(payload.group)
        message += struct.pack('>i', payload.generation_id)
        message += write_short_text(payload.member_id)

        message += struct.pack('>i', len(payload.group_assignment))
        for assignment in payload.group_assignment:
            message += write_short_text(assignment.member_id)
            message += write_int_string(assignment.member_metadata)

        return message

    @classmethod
    def decode_sync_group_response(cls, data):
        """
        Decode bytes to a SyncGroupResponse

        :param bytes data: bytes to decode
        """
        ((correlation_id, error), cur) = relative_unpack('>ih', data, 0)
        (member_assignment, cur) = read_int_string(data, cur)
        return _SyncGroupResponse(error, member_assignment)

    @classmethod
    def encode_sync_group_member_assignment(cls, version, assignments, user_data):
        message = struct.pack('>h', version)
        message += struct.pack('>i', len(assignments))
        for topic, partitions in assignments.items():
            message += write_short_ascii(topic)
            message += struct.pack('>i%si' % len(partitions), len(partitions), *partitions)
        message += write_int_string(user_data)
        return message

    @classmethod
    def decode_sync_group_member_assignment(cls, data):
        """
        Decode bytes to a SyncGroupMemberAssignment

        :param bytes data: bytes to decode
        """

        ((version, num_assignments), cur) = relative_unpack('>hi', data, 0)
        if version != 0:
            raise ProtocolError('Unsupported SyncGroupMemberAssignment version {}'.format(version))
        assignments = {}
        for _i in range(num_assignments):
            (topic, cur) = read_short_ascii(data, cur)
            ((num_partitions,), cur) = relative_unpack('>i', data, cur)
            (partitions, cur) = relative_unpack('>%si' % num_partitions, data, cur)
            assignments[topic] = partitions
        (user_data, cur) = read_int_string(data, cur)
        return _SyncGroupMemberAssignment(version, assignments, user_data)


def create_message(payload, key=None):
    """
    Construct a :class:`Message`

    :param payload: The payload to send to Kafka.
    :type payload: :class:`bytes` or ``None``
    :param key: A key used to route the message when partitioning and to
        determine message identity on a compacted topic.
    :type key: :class:`bytes` or ``None``
    """
    assert payload is None or isinstance(payload, bytes), 'payload={!r} should be bytes or None'.format(payload)
    assert key is None or isinstance(key, bytes), 'key={!r} should be bytes or None'.format(key)
    return Message(0, 0, key, payload)


def create_gzip_message(message_set):
    """
    Construct a gzip-compressed message containing multiple messages

    The given messages will be encoded, compressed, and sent as a single atomic
    message to Kafka.

    :param list message_set: a list of :class:`Message` instances
    """
    encoded_message_set = KafkaCodec._encode_message_set(message_set)

    gzipped = gzip_encode(encoded_message_set)
    return Message(0, CODEC_GZIP, None, gzipped)


def create_snappy_message(message_set):
    """
    Construct a Snappy-compressed message containing multiple messages

    The given messages will be encoded, compressed, and sent as a single atomic
    message to Kafka.

    :param list message_set: a list of :class:`Message` instances
    """
    encoded_message_set = KafkaCodec._encode_message_set(message_set)
    snapped = snappy_encode(encoded_message_set)
    return Message(0, CODEC_SNAPPY, None, snapped)


def create_message_set(requests, codec=CODEC_NONE):
    """
    Create a message set from a list of requests.

    Each request can have a list of messages and its own key.  If codec is
    :data:`CODEC_NONE`, return a list of raw Kafka messages. Otherwise, return
    a list containing a single codec-encoded message.

    :param codec:
        The encoding for the message set, one of the constants:

        - `afkak.CODEC_NONE`
        - `afkak.CODEC_GZIP`
        - `afkak.CODEC_SNAPPY`

    :raises: :exc:`UnsupportedCodecError` for an unsupported codec
    """
    msglist = []
    for req in requests:
        msglist.extend([create_message(m, key=req.key) for m in req.messages])

    if codec == CODEC_NONE:
        return msglist
    elif codec == CODEC_GZIP:
        return [create_gzip_message(msglist)]
    elif codec == CODEC_SNAPPY:
        return [create_snappy_message(msglist)]
    else:
        raise UnsupportedCodecError("Codec 0x%02x unsupported" % codec)
