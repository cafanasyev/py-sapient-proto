"""Descriptor-derived ICD option sets, shared errors, timestamp helpers.

All validation rule sets are read from the compiled proto descriptors
(`proto_options` extensions), so they cannot drift from the .proto files.
"""
from __future__ import annotations

from datetime import datetime, timezone
from functools import cache
from typing import cast

from google.protobuf.descriptor import Descriptor, FieldDescriptor, OneofDescriptor
from google.protobuf.timestamp_pb2 import Timestamp
from sapient_msg import proto_options_pb2


class IcdValidationError(ValueError):
    """A message violates BSI Flex 335 ICD rules (mandatory fields/oneofs)."""


# protoc's --pyi_out types extension descriptors as plain FieldDescriptor, which
# types-protobuf's Extensions[...] signature rejects; confine the cast here.
def _field_opts(f: FieldDescriptor) -> proto_options_pb2.ValidationOptions:
    return cast(
        proto_options_pb2.ValidationOptions,
        f.GetOptions().Extensions[proto_options_pb2.field_options],  # type: ignore[index]
    )


def _oneof_opts(o: OneofDescriptor) -> proto_options_pb2.ValidationOptions:
    return cast(
        proto_options_pb2.ValidationOptions,
        o.GetOptions().Extensions[proto_options_pb2.oneof_options],  # type: ignore[index]
    )


@cache
def mandatory_fields(descriptor: Descriptor) -> frozenset[str]:
    return frozenset(
        f.name for f in descriptor.fields if _field_opts(f).is_mandatory
    )


@cache
def uuid_fields(descriptor: Descriptor) -> frozenset[str]:
    return frozenset(f.name for f in descriptor.fields if _field_opts(f).is_uuid)


@cache
def ulid_fields(descriptor: Descriptor) -> frozenset[str]:
    return frozenset(f.name for f in descriptor.fields if _field_opts(f).is_ulid)


@cache
def mandatory_oneofs(descriptor: Descriptor) -> frozenset[str]:
    return frozenset(
        o.name for o in descriptor.oneofs if _oneof_opts(o).is_mandatory
    )


def datetime_to_pb2(dt: datetime) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def pb2_to_datetime(ts: Timestamp) -> datetime:
    return ts.ToDatetime(tzinfo=timezone.utc)
