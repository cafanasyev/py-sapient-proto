"""Round-trips for error / follow / associated_detection / associated_file models."""
from datetime import datetime, timezone

import pytest
from sapient_msg.bsi_flex_335_v2_0 import (
    associated_detection_pb2,
    associated_file_pb2,
    error_pb2,
    follow_pb2,
)
from sapient_msg_pydantic._options import IcdValidationError, datetime_to_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_detection import (
    AssociatedDetection,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.error import Error
from sapient_msg_pydantic.bsi_flex_335_v2_0.follow import FollowObject

_NODE_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
_OBJECT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAX"

# ---------------------------------------------------------------------------
# associated_file.AssociatedFile
# ---------------------------------------------------------------------------


def _native_associated_file_pb2() -> associated_file_pb2.AssociatedFile:
    return associated_file_pb2.AssociatedFile(type="image", url="http://example.com/a.png")


def _native_associated_file_model() -> AssociatedFile:
    return AssociatedFile(type="image", url="http://example.com/a.png")


def test_associated_file_to_pb2_matches_native() -> None:
    assert _native_associated_file_model().to_pb2() == _native_associated_file_pb2()


def test_associated_file_from_pb2_matches_native() -> None:
    assert (
        AssociatedFile.from_pb2(_native_associated_file_pb2())
        == _native_associated_file_model()
    )


def test_associated_file_double_roundtrip() -> None:
    model = _native_associated_file_model()
    assert AssociatedFile.from_pb2(model.to_pb2()) == model


def test_associated_file_requires_type_and_url() -> None:
    # Both `type` and `url` are mandatory; neither has a natural "unset and
    # still valid" state, so exercise the mandatory-rejection contract
    # instead (mirrors LocationList's precedent in test_geometry_models.py).
    with pytest.raises(IcdValidationError, match="type"):
        AssociatedFile(url="http://example.com/a.png").to_pb2()


# ---------------------------------------------------------------------------
# associated_detection.AssociatedDetection
# ---------------------------------------------------------------------------


def _native_associated_detection_pb2() -> associated_detection_pb2.AssociatedDetection:
    msg = associated_detection_pb2.AssociatedDetection(
        node_id=_NODE_ID,
        object_id=_OBJECT_ID,
        association_type=associated_detection_pb2.AssociationRelation.ASSOCIATION_RELATION_SIBLING,
    )
    msg.timestamp.CopyFrom(
        datetime_to_pb2(datetime(2026, 7, 19, 12, tzinfo=timezone.utc))
    )
    return msg


def _native_associated_detection_model() -> AssociatedDetection:
    return AssociatedDetection(
        timestamp=datetime(2026, 7, 19, 12, tzinfo=timezone.utc),
        node_id=_NODE_ID,
        object_id=_OBJECT_ID,
        association_type=associated_detection_pb2.AssociationRelation.ASSOCIATION_RELATION_SIBLING,
    )


def test_associated_detection_to_pb2_matches_native() -> None:
    assert (
        _native_associated_detection_model().to_pb2()
        == _native_associated_detection_pb2()
    )


def test_associated_detection_from_pb2_matches_native() -> None:
    assert (
        AssociatedDetection.from_pb2(_native_associated_detection_pb2())
        == _native_associated_detection_model()
    )


def test_associated_detection_double_roundtrip() -> None:
    model = _native_associated_detection_model()
    assert AssociatedDetection.from_pb2(model.to_pb2()) == model


def test_associated_detection_unset_optionals_stay_unset() -> None:
    pb = AssociatedDetection(node_id=_NODE_ID, object_id=_OBJECT_ID).to_pb2()
    assert not pb.HasField("timestamp")
    assert AssociatedDetection.from_pb2(pb).timestamp is None
    assert not pb.HasField("association_type")
    assert AssociatedDetection.from_pb2(pb).association_type is None


# ---------------------------------------------------------------------------
# error.Error
# ---------------------------------------------------------------------------


def _native_error_pb2() -> error_pb2.Error:
    msg = error_pb2.Error(packet=b"\x00\x01\x02")
    msg.error_message.extend(["bad checksum", "unknown field"])
    return msg


def _native_error_model() -> Error:
    return Error(
        packet=b"\x00\x01\x02", error_message=["bad checksum", "unknown field"]
    )


def test_error_to_pb2_matches_native() -> None:
    assert _native_error_model().to_pb2() == _native_error_pb2()


def test_error_from_pb2_matches_native() -> None:
    assert Error.from_pb2(_native_error_pb2()) == _native_error_model()


def test_error_double_roundtrip() -> None:
    model = _native_error_model()
    assert Error.from_pb2(model.to_pb2()) == model


def test_error_requires_packet() -> None:
    # `packet` is mandatory and has presence (Optional[bytes] = None); exercise
    # the "stays unset -> mandatory rejection" contract on it directly.
    with pytest.raises(IcdValidationError, match="packet"):
        Error(error_message=["x"]).to_pb2()


# ---------------------------------------------------------------------------
# follow.FollowObject
# ---------------------------------------------------------------------------


def _native_follow_object_pb2() -> follow_pb2.FollowObject:
    return follow_pb2.FollowObject(follow_object_id=_OBJECT_ID)


def _native_follow_object_model() -> FollowObject:
    return FollowObject(follow_object_id=_OBJECT_ID)


def test_follow_object_to_pb2_matches_native() -> None:
    assert _native_follow_object_model().to_pb2() == _native_follow_object_pb2()


def test_follow_object_from_pb2_matches_native() -> None:
    assert (
        FollowObject.from_pb2(_native_follow_object_pb2())
        == _native_follow_object_model()
    )


def test_follow_object_double_roundtrip() -> None:
    model = _native_follow_object_model()
    assert FollowObject.from_pb2(model.to_pb2()) == model


def test_follow_object_requires_non_empty_follow_object_id() -> None:
    # follow_object_id is mandatory but has_presence=False (no `optional` in
    # the .proto), so it defaults to "" rather than None. _require_mandatory()
    # must still treat that default as "missing" -- otherwise an empty
    # FollowObject silently produces ICD-invalid wire data.
    with pytest.raises(IcdValidationError, match="follow_object_id"):
        FollowObject(follow_object_id="").to_pb2()
