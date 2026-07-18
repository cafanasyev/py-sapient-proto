"""Typed usage sample. Checked with `mypy --strict` to prove the generated
stubs support autocomplete and strict typing for consumers."""
from sapient_msg.bsi_flex_335_v2_0.alert_pb2 import Alert
from sapient_msg.bsi_flex_335_v2_0.sapient_message_pb2 import SapientMessage


def build_alert(alert_id: str, description: str) -> SapientMessage:
    msg = SapientMessage()
    msg.timestamp.FromJsonString("2026-07-18T12:00:00Z")
    msg.node_id = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    msg.alert.alert_id = alert_id
    msg.alert.alert_type = Alert.ALERT_TYPE_CRITICAL
    msg.alert.description = description
    return msg


def alert_type_name(msg: SapientMessage) -> str:
    return Alert.AlertType.Name(msg.alert.alert_type)
