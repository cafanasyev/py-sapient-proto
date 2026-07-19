"""Typed usage sample; checked by mypy --strict via the typecheck target."""
from datetime import datetime, timezone

from sapient_msg.bsi_flex_335_v2_0 import alert_pb2, sapient_message_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert import Alert
from sapient_msg_pydantic.bsi_flex_335_v2_0.sapient_message import SapientMessage


def build_alert_envelope(
    node_id: str, description: str
) -> sapient_message_pb2.SapientMessage:
    model = SapientMessage(
        timestamp=datetime.now(timezone.utc),
        node_id=node_id,
        alert=Alert(
            alert_type=alert_pb2.Alert.ALERT_TYPE_WARNING,
            description=description,
        ),
    )
    return model.to_pb2()


def parse_alert_envelope(msg: sapient_message_pb2.SapientMessage) -> str:
    model = SapientMessage.from_pb2(msg)
    if model.alert is None or model.alert.description is None:
        return ""
    return model.alert.description
