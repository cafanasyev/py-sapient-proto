"""SapientModel base behavior via a minimal concrete model."""

import pytest
from pydantic import ValidationError
from sapient_msg.bsi_flex_335_v2_0.sapient_message_pb2 import SapientMessage
from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic._options import IcdValidationError


class ProbeModel(SapientModel):
    pb2_cls = SapientMessage
    node_id: str | None = None
    destination_id: str | None = None
    timestamp: str | None = None  # stand-in; mandatory in the proto


def test_uuid_format_enforced_at_construction() -> None:
    with pytest.raises(ValidationError, match="node_id"):
        ProbeModel(node_id="not-a-uuid")


def test_valid_uuid_accepted() -> None:
    m = ProbeModel(node_id="f47ac10b-58cc-4372-a567-0e02b2c3d479")
    assert m.node_id is not None


def test_unset_uuid_field_allowed_at_construction() -> None:
    ProbeModel()  # construction never enforces mandatory-ness


def test_require_mandatory_lists_all_missing() -> None:
    with pytest.raises(IcdValidationError) as exc:
        ProbeModel()._require_mandatory()
    assert "timestamp" in str(exc.value)
    assert "node_id" in str(exc.value)
