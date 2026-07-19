"""Serialization round-trips: bytes and JSON (the json_format requirement)."""
from google.protobuf import json_format
from sapient_msg.bsi_flex_335_v2_0.alert_pb2 import Alert
from sapient_msg.bsi_flex_335_v2_0.sapient_message_pb2 import SapientMessage


def _sample_message() -> SapientMessage:
    msg = SapientMessage()
    msg.timestamp.FromJsonString("2026-07-18T12:00:00Z")
    msg.node_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    msg.alert.alert_id = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
    msg.alert.alert_type = Alert.ALERT_TYPE_WARNING
    msg.alert.priority = Alert.DISCRETE_PRIORITY_HIGH
    msg.alert.description = "sample alert"
    return msg


def test_bytes_roundtrip() -> None:
    msg = _sample_message()
    parsed = SapientMessage.FromString(msg.SerializeToString())
    assert parsed == msg


def test_json_roundtrip() -> None:
    msg = _sample_message()
    json_str = json_format.MessageToJson(msg)
    parsed = json_format.Parse(json_str, SapientMessage())
    assert parsed == msg


def test_json_uses_proto_field_casing() -> None:
    json_str = json_format.MessageToJson(
        _sample_message(), preserving_proto_field_name=True
    )
    assert '"node_id"' in json_str
    assert '"alert_type": "ALERT_TYPE_WARNING"' in json_str


def test_enum_constants_resolve_by_name() -> None:
    assert Alert.AlertType.Name(Alert.ALERT_TYPE_WARNING) == "ALERT_TYPE_WARNING"
    assert Alert.AlertType.Value("ALERT_TYPE_CRITICAL") == Alert.ALERT_TYPE_CRITICAL
