"""Round-trips for alert / alert_ack models."""
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from sapient_msg.bsi_flex_335_v2_0 import (
    alert_ack_pb2,
    alert_pb2,
    associated_detection_pb2,
    associated_file_pb2,
    location_pb2,
    range_bearing_pb2,
)
from sapient_msg_pydantic._options import datetime_to_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert import Alert
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert_ack import AlertAck
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_detection import (
    AssociatedDetection,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import RangeBearing

_ALERT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
_REGION_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAW"
_NODE_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
_OBJECT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAX"

# ---------------------------------------------------------------------------
# shared builders (associated_file / associated_detection / location /
# range_bearing) reused across the Alert variants below
# ---------------------------------------------------------------------------


def _native_associated_file_pb2() -> associated_file_pb2.AssociatedFile:
    return associated_file_pb2.AssociatedFile(type="image", url="http://example.com/a.png")


def _native_associated_file_model() -> AssociatedFile:
    return AssociatedFile(type="image", url="http://example.com/a.png")


def _native_associated_detection_pb2() -> associated_detection_pb2.AssociatedDetection:
    msg = associated_detection_pb2.AssociatedDetection(
        node_id=_NODE_ID,
        object_id=_OBJECT_ID,
        association_type=associated_detection_pb2.AssociationRelation.ASSOCIATION_RELATION_PARENT,
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
        association_type=associated_detection_pb2.AssociationRelation.ASSOCIATION_RELATION_PARENT,
    )


def _native_location_pb2() -> location_pb2.Location:
    return location_pb2.Location(
        x=1.5,
        y=-2.5,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )


def _native_location_model() -> Location:
    return Location(
        x=1.5,
        y=-2.5,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )


def _native_range_bearing_model() -> RangeBearing:
    return RangeBearing(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _native_range_bearing_pb2() -> range_bearing_pb2.RangeBearing:
    return range_bearing_pb2.RangeBearing(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


# ---------------------------------------------------------------------------
# alert.Alert (location leg of location_oneof; exercises every scalar field)
# ---------------------------------------------------------------------------


def _native_alert_location_pb2() -> alert_pb2.Alert:
    msg = alert_pb2.Alert(
        alert_id=_ALERT_ID,
        alert_type=alert_pb2.Alert.AlertType.ALERT_TYPE_WARNING,
        status=alert_pb2.Alert.AlertStatus.ALERT_STATUS_ACTIVE,
    )
    msg.description = "something happened"
    msg.location.CopyFrom(_native_location_pb2())
    msg.region_id = _REGION_ID
    msg.priority = alert_pb2.Alert.DiscretePriority.DISCRETE_PRIORITY_HIGH
    msg.ranking = 0.75
    msg.confidence = 0.875
    msg.associated_file.extend([_native_associated_file_pb2()])
    msg.associated_detection.extend([_native_associated_detection_pb2()])
    msg.additional_information = "extra info"
    return msg


def _native_alert_location_model() -> Alert:
    return Alert(
        alert_id=_ALERT_ID,
        alert_type=alert_pb2.Alert.AlertType.ALERT_TYPE_WARNING,
        status=alert_pb2.Alert.AlertStatus.ALERT_STATUS_ACTIVE,
        description="something happened",
        location=_native_location_model(),
        region_id=_REGION_ID,
        priority=alert_pb2.Alert.DiscretePriority.DISCRETE_PRIORITY_HIGH,
        ranking=0.75,
        confidence=0.875,
        associated_file=[_native_associated_file_model()],
        associated_detection=[_native_associated_detection_model()],
        additional_information="extra info",
    )


def test_alert_to_pb2_matches_native() -> None:
    assert _native_alert_location_model().to_pb2() == _native_alert_location_pb2()


def test_alert_from_pb2_matches_native() -> None:
    assert (
        Alert.from_pb2(_native_alert_location_pb2()) == _native_alert_location_model()
    )


def test_alert_double_roundtrip() -> None:
    model = _native_alert_location_model()
    assert Alert.from_pb2(model.to_pb2()) == model


def test_alert_unset_optionals_stay_unset() -> None:
    pb = Alert(alert_id=_ALERT_ID).to_pb2()
    assert not pb.HasField("description")
    assert Alert.from_pb2(pb).description is None


# ---------------------------------------------------------------------------
# alert.Alert (range_bearing leg of location_oneof)
# ---------------------------------------------------------------------------


def test_alert_range_bearing_variant_roundtrips() -> None:
    model = Alert(alert_id=_ALERT_ID, range_bearing=_native_range_bearing_model())
    pb = model.to_pb2()
    assert pb.HasField("range_bearing")
    assert not pb.HasField("location")
    assert pb.range_bearing == _native_range_bearing_pb2()
    assert Alert.from_pb2(pb) == model


# ---------------------------------------------------------------------------
# alert.Alert ULID behaviour
# ---------------------------------------------------------------------------


def test_alert_auto_generates_valid_ulid() -> None:
    model = Alert()
    assert model.alert_id is not None
    assert len(model.alert_id) == 26


def test_alert_rejects_invalid_alert_id() -> None:
    with pytest.raises(ValidationError):
        Alert(alert_id="not-a-ulid")


# ---------------------------------------------------------------------------
# alert_ack.AlertAck
# ---------------------------------------------------------------------------


def _native_alert_ack_pb2() -> alert_ack_pb2.AlertAck:
    msg = alert_ack_pb2.AlertAck(
        alert_id=_ALERT_ID,
        alert_ack_status=alert_ack_pb2.AlertAck.AlertAckStatus.ALERT_ACK_STATUS_REJECTED,
    )
    msg.reason.extend(["bad signal", "duplicate"])
    return msg


def _native_alert_ack_model() -> AlertAck:
    return AlertAck(
        alert_id=_ALERT_ID,
        reason=["bad signal", "duplicate"],
        alert_ack_status=alert_ack_pb2.AlertAck.AlertAckStatus.ALERT_ACK_STATUS_REJECTED,
    )


def test_alert_ack_to_pb2_matches_native() -> None:
    assert _native_alert_ack_model().to_pb2() == _native_alert_ack_pb2()


def test_alert_ack_from_pb2_matches_native() -> None:
    assert AlertAck.from_pb2(_native_alert_ack_pb2()) == _native_alert_ack_model()


def test_alert_ack_double_roundtrip() -> None:
    model = _native_alert_ack_model()
    assert AlertAck.from_pb2(model.to_pb2()) == model


def test_alert_ack_unset_optionals_stay_unset() -> None:
    # AlertAck has no optional scalar besides the mandatory ones + repeated
    # `reason`; exercise the "stays unset" contract via the repeated field
    # (mirrors LocationList's precedent in test_geometry_models.py).
    pb = AlertAck(
        alert_id=_ALERT_ID,
        alert_ack_status=alert_ack_pb2.AlertAck.AlertAckStatus.ALERT_ACK_STATUS_ACCEPTED,
    ).to_pb2()
    assert list(pb.reason) == []
    assert AlertAck.from_pb2(pb).reason == []
