# -*- coding: utf-8 -*-
# Copyright 2016 Cyan, Inc.
# Copyright 2018, 2019, 2020 Ciena Corporation

from __future__ import absolute_import

from ._group import ConsumerGroup
from .client import KafkaClient
from .common import (
    CODEC_GZIP, CODEC_LZ4, CODEC_NONE, CODEC_SNAPPY, OFFSET_COMMITTED,
    OFFSET_EARLIEST, OFFSET_LATEST,
)
from .consumer import Consumer
from .kafkacodec import create_message, create_message_set
from .partitioner import HashedPartitioner, RoundRobinPartitioner
from .producer import Producer

# Note, you need to bump the version in setup.py as well
__title__ = 'afkak'
__version__ = "20.9.0"  # Makefile parses this. Retain formatting.
__author__ = 'Robert Thille'
__license__ = 'Apache License 2.0'

__all__ = [
    'KafkaClient', 'Producer', 'Consumer', 'ConsumerGroup',
    'RoundRobinPartitioner', 'HashedPartitioner',
    'create_message', 'create_message_set',
    'CODEC_NONE', 'CODEC_GZIP', 'CODEC_LZ4', 'CODEC_SNAPPY',
    'OFFSET_EARLIEST', 'OFFSET_LATEST', 'OFFSET_COMMITTED',
]
