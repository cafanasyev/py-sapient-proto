"""Descriptor-derived ICD option sets: verify against known proto facts."""
from datetime import datetime, timezone

from sapient_msg.bsi_flex_335_v2_0.alert_pb2 import Alert
from sapient_msg.bsi_flex_335_v2_0.registration_pb2 import Registration
from sapient_msg.bsi_flex_335_v2_0.sapient_message_pb2 import SapientMessage
from sapient_msg_pydantic._options import (
    datetime_to_pb2,
    mandatory_fields,
    mandatory_oneofs,
    pb2_to_datetime,
    ulid_fields,
    uuid_fields,
)


def test_mandatory_fields_registration() -> None:
    fields = mandatory_fields(Registration.DESCRIPTOR)
    assert {"node_definition", "icd_version", "capabilities"} <= fields
    assert "name" not in fields


def test_uuid_fields_sapient_message() -> None:
    assert uuid_fields(SapientMessage.DESCRIPTOR) == {"node_id", "destination_id"}


def test_ulid_fields_alert() -> None:
    assert "alert_id" in ulid_fields(Alert.DESCRIPTOR)


def test_mandatory_oneof_content() -> None:
    assert mandatory_oneofs(SapientMessage.DESCRIPTOR) == {"content"}


def test_timestamp_roundtrip() -> None:
    dt = datetime(2026, 7, 19, 12, 0, 0, tzinfo=timezone.utc)
    assert pb2_to_datetime(datetime_to_pb2(dt)) == dt
