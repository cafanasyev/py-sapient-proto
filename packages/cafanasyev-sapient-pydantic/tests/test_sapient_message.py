"""SapientMessage wrapper: oneof enforcement + full-envelope round-trips."""
from datetime import datetime, timezone

import pytest
from sapient_msg.bsi_flex_335_v2_0 import alert_pb2, sapient_message_pb2
from sapient_msg_pydantic._options import IcdValidationError, datetime_to_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert import Alert
from sapient_msg_pydantic.bsi_flex_335_v2_0.sapient_message import SapientMessage

NODE_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
TS = datetime(2026, 7, 19, 12, 0, 0, tzinfo=timezone.utc)
ALERT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"


def _native_pb2() -> sapient_message_pb2.SapientMessage:
    msg = sapient_message_pb2.SapientMessage(node_id=NODE_ID)
    msg.timestamp.CopyFrom(datetime_to_pb2(TS))
    msg.alert.alert_id = ALERT_ID
    msg.alert.alert_type = alert_pb2.Alert.ALERT_TYPE_WARNING
    return msg


def _native_model() -> SapientMessage:
    return SapientMessage(
        timestamp=TS,
        node_id=NODE_ID,
        alert=Alert(
            alert_id=ALERT_ID,
            alert_type=alert_pb2.Alert.ALERT_TYPE_WARNING,
        ),
    )


def test_to_pb2_matches_native() -> None:
    assert _native_model().to_pb2() == _native_pb2()


def test_from_pb2_matches_native() -> None:
    assert SapientMessage.from_pb2(_native_pb2()) == _native_model()


def test_double_roundtrip() -> None:
    model = _native_model()
    assert SapientMessage.from_pb2(model.to_pb2()) == model


def test_empty_content_oneof_rejected() -> None:
    with pytest.raises(IcdValidationError, match="content"):
        SapientMessage(timestamp=TS, node_id=NODE_ID).to_pb2()


def test_double_content_oneof_rejected() -> None:
    from sapient_msg_pydantic.bsi_flex_335_v2_0.error import Error

    with pytest.raises(IcdValidationError, match="content"):
        SapientMessage(
            timestamp=TS, node_id=NODE_ID, alert=Alert(alert_id=ALERT_ID),
            error=Error(),
        ).to_pb2()


def test_missing_mandatory_fields_listed() -> None:
    with pytest.raises(IcdValidationError) as exc:
        SapientMessage(alert=Alert(alert_id=ALERT_ID)).to_pb2()
    assert "timestamp" in str(exc.value)
    assert "node_id" in str(exc.value)


def test_bad_node_id_rejected_at_construction() -> None:
    from pydantic import ValidationError

    with pytest.raises(ValidationError, match="node_id"):
        SapientMessage(node_id="not-a-uuid")
