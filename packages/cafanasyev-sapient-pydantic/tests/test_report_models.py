"""Round-trips for status_report / detection_report models.

Every nested model gets the three-assertion round-trip core used throughout
this package (native-pb2 built independently of the pydantic model; both
directions checked, plus a double round-trip), via `_assert_roundtrip`, and a
fourth assertion exercising either an optional field staying unset, a
mandatory-field rejection, a oneof-exclusivity rejection, or (for
`report_id`/`object_id`) ULID auto-generation behaviour.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sapient_msg.bsi_flex_335_v2_0 import (
    associated_detection_pb2,
    associated_file_pb2,
    detection_report_pb2,
    location_pb2,
    range_bearing_pb2,
    status_report_pb2,
    velocity_pb2,
)
from sapient_msg_pydantic._options import IcdValidationError, datetime_to_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_detection import (
    AssociatedDetection,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.detection_report import (
    Behaviour,
    DerivedDetection,
    DetectionReport,
    DetectionReportClassification,
    PredictedLocation,
    Signal,
    SubClass,
    TrackObjectInfo,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
    RangeBearing,
    RangeBearingCone,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.status_report import (
    Power,
    Status,
    StatusReport,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.velocity import ENUVelocity

SR = status_report_pb2.StatusReport
DR = detection_report_pb2.DetectionReport

_REPORT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
_ACTIVE_TASK_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAW"
_OBJECT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAX"
_TASK_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAY"
_NODE_ID = "7c9e6679-7425-40de-944b-e07fc1f90ae7"
_DERIVED_OBJECT_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAZ"


def _assert_roundtrip(model_cls, model_fn, pb2_fn) -> None:  # type: ignore[no-untyped-def]
    model = model_fn()
    pb2_msg = pb2_fn()
    assert model.to_pb2() == pb2_msg
    assert model_cls.from_pb2(pb2_msg) == model
    assert model_cls.from_pb2(model.to_pb2()) == model


# ---------------------------------------------------------------------------
# shared geometry builders
# ---------------------------------------------------------------------------


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


def _native_range_bearing_pb2() -> range_bearing_pb2.RangeBearing:
    return range_bearing_pb2.RangeBearing(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _native_range_bearing_model() -> RangeBearing:
    return RangeBearing(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _native_range_bearing_cone_pb2() -> range_bearing_pb2.RangeBearingCone:
    return range_bearing_pb2.RangeBearingCone(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _native_range_bearing_cone_model() -> RangeBearingCone:
    return RangeBearingCone(
        elevation=1.1,
        azimuth=2.2,
        range=3.3,
        coordinate_system=range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M,
        datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _native_location_or_range_bearing_pb2() -> range_bearing_pb2.LocationOrRangeBearing:
    msg = range_bearing_pb2.LocationOrRangeBearing()
    msg.range_bearing.CopyFrom(_native_range_bearing_cone_pb2())
    return msg


def _native_location_or_range_bearing_model() -> LocationOrRangeBearing:
    return LocationOrRangeBearing(range_bearing=_native_range_bearing_cone_model())


# ---------------------------------------------------------------------------
# status_report.Power
# ---------------------------------------------------------------------------


def _native_power_pb2() -> status_report_pb2.StatusReport.Power:
    msg = SR.Power(level=75)
    msg.source = SR.PowerSource.POWERSOURCE_INTERNAL_BATTERY
    msg.status = SR.PowerStatus.POWERSTATUS_OK
    return msg


def _native_power_model() -> Power:
    return Power(
        level=75,
        source=SR.PowerSource.POWERSOURCE_INTERNAL_BATTERY,
        status=SR.PowerStatus.POWERSTATUS_OK,
    )


def test_power_to_pb2_matches_native() -> None:
    assert _native_power_model().to_pb2() == _native_power_pb2()


def test_power_from_pb2_matches_native() -> None:
    assert Power.from_pb2(_native_power_pb2()) == _native_power_model()


def test_power_double_roundtrip() -> None:
    model = _native_power_model()
    assert Power.from_pb2(model.to_pb2()) == model


def test_power_source_and_status_default_to_unspecified() -> None:
    # source/status have no proto presence -> non-optional, default 0
    # (*_UNSPECIFIED) when omitted; no HasField exists for either.
    model = Power(level=10)
    pb = model.to_pb2()
    assert pb.source == SR.PowerSource.POWERSOURCE_UNSPECIFIED
    assert pb.status == SR.PowerStatus.POWERSTATUS_UNSPECIFIED
    assert Power.from_pb2(pb).source == SR.PowerSource.POWERSOURCE_UNSPECIFIED
    assert Power.from_pb2(pb).status == SR.PowerStatus.POWERSTATUS_UNSPECIFIED


# ---------------------------------------------------------------------------
# status_report.Status
# ---------------------------------------------------------------------------


def _native_status_pb2() -> status_report_pb2.StatusReport.Status:
    return SR.Status(
        status_level=SR.StatusLevel.STATUS_LEVEL_WARNING_STATUS,
        status_value="Raining",
        status_type=SR.StatusType.STATUS_TYPE_WEATHER,
    )


def _native_status_model() -> Status:
    return Status(
        status_level=SR.StatusLevel.STATUS_LEVEL_WARNING_STATUS,
        status_value="Raining",
        status_type=SR.StatusType.STATUS_TYPE_WEATHER,
    )


def test_status_to_pb2_matches_native() -> None:
    assert _native_status_model().to_pb2() == _native_status_pb2()


def test_status_from_pb2_matches_native() -> None:
    assert Status.from_pb2(_native_status_pb2()) == _native_status_model()


def test_status_double_roundtrip() -> None:
    model = _native_status_model()
    assert Status.from_pb2(model.to_pb2()) == model


def test_status_requires_status_type() -> None:
    with pytest.raises(IcdValidationError, match="status_type"):
        Status().to_pb2()


# ---------------------------------------------------------------------------
# status_report.StatusReport
# ---------------------------------------------------------------------------


def _native_status_report_pb2() -> status_report_pb2.StatusReport:
    msg = SR(
        report_id=_REPORT_ID,
        system=SR.System.SYSTEM_OK,
        info=SR.Info.INFO_NEW,
        mode="patrol",
    )
    msg.active_task_id = _ACTIVE_TASK_ID
    msg.power.CopyFrom(_native_power_pb2())
    msg.node_location.CopyFrom(_native_location_pb2())
    msg.field_of_view.CopyFrom(_native_location_or_range_bearing_pb2())
    msg.obscuration.extend([_native_location_or_range_bearing_pb2()])
    msg.status.extend([_native_status_pb2()])
    msg.coverage.extend([_native_location_or_range_bearing_pb2()])
    return msg


def _native_status_report_model() -> StatusReport:
    return StatusReport(
        report_id=_REPORT_ID,
        system=SR.System.SYSTEM_OK,
        info=SR.Info.INFO_NEW,
        active_task_id=_ACTIVE_TASK_ID,
        mode="patrol",
        power=_native_power_model(),
        node_location=_native_location_model(),
        field_of_view=_native_location_or_range_bearing_model(),
        obscuration=[_native_location_or_range_bearing_model()],
        status=[_native_status_model()],
        coverage=[_native_location_or_range_bearing_model()],
    )


def test_status_report_to_pb2_matches_native() -> None:
    assert _native_status_report_model().to_pb2() == _native_status_report_pb2()


def test_status_report_from_pb2_matches_native() -> None:
    assert (
        StatusReport.from_pb2(_native_status_report_pb2())
        == _native_status_report_model()
    )


def test_status_report_double_roundtrip() -> None:
    model = _native_status_report_model()
    assert StatusReport.from_pb2(model.to_pb2()) == model


def test_status_report_unset_optionals_stay_unset() -> None:
    pb = StatusReport(
        report_id=_REPORT_ID,
        system=SR.System.SYSTEM_OK,
        info=SR.Info.INFO_NEW,
        mode="patrol",
    ).to_pb2()
    assert not pb.HasField("active_task_id")
    assert StatusReport.from_pb2(pb).active_task_id is None


def test_status_report_auto_generates_valid_ulid() -> None:
    model = StatusReport(
        system=SR.System.SYSTEM_OK, info=SR.Info.INFO_NEW, mode="patrol"
    )
    assert model.report_id is not None
    assert len(model.report_id) == 26


def test_status_report_requires_mandatory_fields() -> None:
    with pytest.raises(IcdValidationError, match="mode"):
        StatusReport(report_id=_REPORT_ID).to_pb2()


# ---------------------------------------------------------------------------
# detection_report.TrackObjectInfo (used for both track_info and object_info)
# ---------------------------------------------------------------------------


def _native_track_object_info_pb2() -> (
    detection_report_pb2.DetectionReport.TrackObjectInfo
):
    return DR.TrackObjectInfo(type="colour", value="red", error=0.25)


def _native_track_object_info_model() -> TrackObjectInfo:
    return TrackObjectInfo(type="colour", value="red", error=0.25)


def test_track_object_info_to_pb2_matches_native() -> None:
    assert (
        _native_track_object_info_model().to_pb2()
        == _native_track_object_info_pb2()
    )


def test_track_object_info_from_pb2_matches_native() -> None:
    assert (
        TrackObjectInfo.from_pb2(_native_track_object_info_pb2())
        == _native_track_object_info_model()
    )


def test_track_object_info_double_roundtrip() -> None:
    model = _native_track_object_info_model()
    assert TrackObjectInfo.from_pb2(model.to_pb2()) == model


def test_track_object_info_requires_type_and_value() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        TrackObjectInfo(value="red").to_pb2()


# ---------------------------------------------------------------------------
# detection_report.SubClass (self-referential)
# ---------------------------------------------------------------------------


def _native_sub_class_pb2() -> detection_report_pb2.DetectionReport.SubClass:
    leaf = DR.SubClass(type="quadcopter", confidence=0.9375, level=1)
    root = DR.SubClass(type="uav", confidence=0.875, level=0)
    root.sub_class.extend([leaf])
    return root


def _native_sub_class_model() -> SubClass:
    leaf = SubClass(type="quadcopter", confidence=0.9375, level=1)
    return SubClass(type="uav", confidence=0.875, level=0, sub_class=[leaf])


def test_sub_class_recursive_roundtrip() -> None:
    _assert_roundtrip(SubClass, _native_sub_class_model, _native_sub_class_pb2)


def test_sub_class_requires_type_and_level() -> None:
    with pytest.raises(IcdValidationError, match="level"):
        SubClass(type="uav").to_pb2()


# ---------------------------------------------------------------------------
# detection_report.DetectionReportClassification
# ---------------------------------------------------------------------------


def _native_classification_pb2() -> (
    detection_report_pb2.DetectionReport.DetectionReportClassification
):
    msg = DR.DetectionReportClassification(type="air", confidence=0.9375)
    msg.sub_class.extend([_native_sub_class_pb2()])
    return msg


def _native_classification_model() -> DetectionReportClassification:
    return DetectionReportClassification(
        type="air", confidence=0.9375, sub_class=[_native_sub_class_model()]
    )


def test_classification_roundtrip() -> None:
    _assert_roundtrip(
        DetectionReportClassification,
        _native_classification_model,
        _native_classification_pb2,
    )


def test_classification_requires_type() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        DetectionReportClassification().to_pb2()


# ---------------------------------------------------------------------------
# detection_report.Behaviour
# ---------------------------------------------------------------------------


def _native_behaviour_pb2() -> detection_report_pb2.DetectionReport.Behaviour:
    return DR.Behaviour(type="loitering", confidence=0.75)


def _native_behaviour_model() -> Behaviour:
    return Behaviour(type="loitering", confidence=0.75)


def test_behaviour_roundtrip() -> None:
    _assert_roundtrip(Behaviour, _native_behaviour_model, _native_behaviour_pb2)


def test_behaviour_requires_type() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        Behaviour().to_pb2()


# ---------------------------------------------------------------------------
# detection_report.Signal
# ---------------------------------------------------------------------------


def _native_signal_pb2() -> detection_report_pb2.DetectionReport.Signal:
    return DR.Signal(
        amplitude=10.0,
        start_frequency=100.0,
        centre_frequency=150.0,
        stop_frequency=200.0,
        pulse_duration=0.5,
    )


def _native_signal_model() -> Signal:
    return Signal(
        amplitude=10.0,
        start_frequency=100.0,
        centre_frequency=150.0,
        stop_frequency=200.0,
        pulse_duration=0.5,
    )


def test_signal_roundtrip() -> None:
    _assert_roundtrip(Signal, _native_signal_model, _native_signal_pb2)


def test_signal_requires_amplitude_and_centre_frequency() -> None:
    with pytest.raises(IcdValidationError, match="centre_frequency"):
        Signal(amplitude=10.0).to_pb2()


# ---------------------------------------------------------------------------
# detection_report.PredictedLocation
# ---------------------------------------------------------------------------


def _native_predicted_location_pb2() -> (
    detection_report_pb2.DetectionReport.PredictedLocation
):
    msg = DR.PredictedLocation()
    msg.location.CopyFrom(_native_location_pb2())
    msg.predicted_timestamp.CopyFrom(
        datetime_to_pb2(datetime(2026, 7, 19, 13, tzinfo=timezone.utc))
    )
    return msg


def _native_predicted_location_model() -> PredictedLocation:
    return PredictedLocation(
        location=_native_location_model(),
        predicted_timestamp=datetime(2026, 7, 19, 13, tzinfo=timezone.utc),
    )


def test_predicted_location_roundtrip() -> None:
    _assert_roundtrip(
        PredictedLocation,
        _native_predicted_location_model,
        _native_predicted_location_pb2,
    )


def test_predicted_location_unset_optionals_stay_unset() -> None:
    pb = PredictedLocation(location=_native_location_model()).to_pb2()
    assert not pb.HasField("predicted_timestamp")
    assert PredictedLocation.from_pb2(pb).predicted_timestamp is None


# ---------------------------------------------------------------------------
# detection_report.DerivedDetection
# ---------------------------------------------------------------------------


def _native_derived_detection_pb2() -> (
    detection_report_pb2.DetectionReport.DerivedDetection
):
    msg = DR.DerivedDetection(node_id=_NODE_ID, object_id=_DERIVED_OBJECT_ID)
    msg.timestamp.CopyFrom(
        datetime_to_pb2(datetime(2026, 7, 19, 14, tzinfo=timezone.utc))
    )
    return msg


def _native_derived_detection_model() -> DerivedDetection:
    return DerivedDetection(
        timestamp=datetime(2026, 7, 19, 14, tzinfo=timezone.utc),
        node_id=_NODE_ID,
        object_id=_DERIVED_OBJECT_ID,
    )


def test_derived_detection_roundtrip() -> None:
    _assert_roundtrip(
        DerivedDetection, _native_derived_detection_model, _native_derived_detection_pb2
    )


def test_derived_detection_requires_node_id_and_object_id() -> None:
    with pytest.raises(IcdValidationError, match="node_id"):
        DerivedDetection(object_id=_DERIVED_OBJECT_ID).to_pb2()


# ---------------------------------------------------------------------------
# detection_report.DetectionReport (location leg; the "everything" build:
# location, object_info, classification tree with recursive SubClass, signal)
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
        datetime_to_pb2(datetime(2026, 7, 19, 15, tzinfo=timezone.utc))
    )
    return msg


def _native_associated_detection_model() -> AssociatedDetection:
    return AssociatedDetection(
        timestamp=datetime(2026, 7, 19, 15, tzinfo=timezone.utc),
        node_id=_NODE_ID,
        object_id=_OBJECT_ID,
        association_type=associated_detection_pb2.AssociationRelation.ASSOCIATION_RELATION_PARENT,
    )


def _native_detection_report_location_pb2() -> detection_report_pb2.DetectionReport:
    msg = DR(report_id=_REPORT_ID, object_id=_OBJECT_ID)
    msg.task_id = _TASK_ID
    msg.state = "tracking"
    msg.location.CopyFrom(_native_location_pb2())
    msg.detection_confidence = 0.875
    msg.track_info.extend([_native_track_object_info_pb2()])
    msg.prediction_location.CopyFrom(_native_predicted_location_pb2())
    msg.object_info.extend([_native_track_object_info_pb2()])
    msg.classification.extend([_native_classification_pb2()])
    msg.behaviour.extend([_native_behaviour_pb2()])
    msg.associated_file.extend([_native_associated_file_pb2()])
    msg.signal.extend([_native_signal_pb2()])
    msg.associated_detection.extend([_native_associated_detection_pb2()])
    msg.derived_detection.extend([_native_derived_detection_pb2()])
    msg.enu_velocity.CopyFrom(
        velocity_pb2.ENUVelocity(east_rate=1.0, north_rate=2.0, up_rate=0.0)
    )
    msg.colour = "grey"
    msg.id = "tail-123"
    return msg


def _native_detection_report_location_model() -> DetectionReport:
    return DetectionReport(
        report_id=_REPORT_ID,
        object_id=_OBJECT_ID,
        task_id=_TASK_ID,
        state="tracking",
        location=_native_location_model(),
        detection_confidence=0.875,
        track_info=[_native_track_object_info_model()],
        prediction_location=_native_predicted_location_model(),
        object_info=[_native_track_object_info_model()],
        classification=[_native_classification_model()],
        behaviour=[_native_behaviour_model()],
        associated_file=[_native_associated_file_model()],
        signal=[_native_signal_model()],
        associated_detection=[_native_associated_detection_model()],
        derived_detection=[_native_derived_detection_model()],
        enu_velocity=ENUVelocity(east_rate=1.0, north_rate=2.0, up_rate=0.0),
        colour="grey",
        id="tail-123",
    )


def test_detection_report_to_pb2_matches_native() -> None:
    assert (
        _native_detection_report_location_model().to_pb2()
        == _native_detection_report_location_pb2()
    )


def test_detection_report_from_pb2_matches_native() -> None:
    assert (
        DetectionReport.from_pb2(_native_detection_report_location_pb2())
        == _native_detection_report_location_model()
    )


def test_detection_report_double_roundtrip() -> None:
    model = _native_detection_report_location_model()
    assert DetectionReport.from_pb2(model.to_pb2()) == model


def test_detection_report_unset_optionals_stay_unset() -> None:
    pb = DetectionReport(
        report_id=_REPORT_ID, object_id=_OBJECT_ID, location=_native_location_model()
    ).to_pb2()
    assert not pb.HasField("task_id")
    assert DetectionReport.from_pb2(pb).task_id is None


# ---------------------------------------------------------------------------
# detection_report.DetectionReport (range_bearing leg of location_oneof)
# ---------------------------------------------------------------------------


def test_detection_report_range_bearing_variant_roundtrips() -> None:
    model = DetectionReport(
        report_id=_REPORT_ID,
        object_id=_OBJECT_ID,
        range_bearing=_native_range_bearing_model(),
    )
    pb = model.to_pb2()
    assert pb.HasField("range_bearing")
    assert not pb.HasField("location")
    assert pb.range_bearing == _native_range_bearing_pb2()
    assert DetectionReport.from_pb2(pb) == model


# ---------------------------------------------------------------------------
# detection_report.DetectionReport ULID / mandatory-oneof behaviour
# ---------------------------------------------------------------------------


def test_detection_report_auto_generates_valid_report_id() -> None:
    model = DetectionReport(object_id=_OBJECT_ID, location=_native_location_model())
    assert model.report_id is not None
    assert len(model.report_id) == 26


def test_detection_report_object_id_not_auto_generated() -> None:
    # object_id is a reference to the persistent detected object, not an
    # identity this report mints itself -- it stays None until set by the
    # caller (matches `external/sapient/builder/detection_report.py`, which
    # defaults it to `""` rather than a fresh ULID).
    model = DetectionReport(location=_native_location_model())
    assert model.object_id is None


def test_detection_report_requires_exactly_one_location_oneof_member() -> None:
    model = DetectionReport(report_id=_REPORT_ID, object_id=_OBJECT_ID)
    with pytest.raises(IcdValidationError, match="location_oneof"):
        model.to_pb2()


def test_detection_report_rejects_both_location_oneof_members_set() -> None:
    model = DetectionReport(
        report_id=_REPORT_ID,
        object_id=_OBJECT_ID,
        location=_native_location_model(),
        range_bearing=_native_range_bearing_model(),
    )
    with pytest.raises(IcdValidationError, match="location_oneof"):
        model.to_pb2()
