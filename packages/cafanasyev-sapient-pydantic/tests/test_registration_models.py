"""Round-trips for registration / registration_ack models (largest module).

Every nested model gets the same three-assertion round-trip core used
throughout this package (native-pb2 built independently of the pydantic
model; both directions checked, plus a double round-trip), via
`_assert_roundtrip`, and a fourth assertion exercising either an optional
field staying unset, a mandatory-field rejection, or (for the two
mandatory-oneof messages) oneof-exclusivity.
"""
from __future__ import annotations

import pytest
from sapient_msg.bsi_flex_335_v2_0 import (
    location_pb2,
    range_bearing_pb2,
    registration_ack_pb2,
    registration_pb2,
    velocity_pb2,
)
from sapient_msg_pydantic._options import IcdValidationError
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
    RangeBearingCone,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.registration import (
    ICD_VERSION,
    BehaviourDefinition,
    BehaviourFilterDefinition,
    Capability,
    ClassDefinition,
    ClassFilterDefinition,
    Command,
    ConfigurationData,
    DetectionClassDefinition,
    DetectionDefinition,
    DetectionReport,
    Duration,
    ExtensionSubclass,
    FilterParameter,
    GeometricError,
    LocationType,
    ModeDefinition,
    ModeParameter,
    NodeDefinition,
    PerformanceValue,
    RegionDefinition,
    Registration,
    StatusDefinition,
    StatusReport,
    SubClass,
    SubClassFilterDefinition,
    TaskDefinition,
    TaxonomyDockDefinition,
    VelocityType,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.registration_ack import RegistrationAck
from sapient_msg_pydantic.bsi_flex_335_v2_0.velocity import ENUVelocityUnits

R = registration_pb2.Registration


def _assert_roundtrip(model_cls, model_fn, pb2_fn) -> None:  # type: ignore[no-untyped-def]
    model = model_fn()
    pb2_msg = pb2_fn()
    assert model.to_pb2() == pb2_msg
    assert model_cls.from_pb2(pb2_msg) == model
    assert model_cls.from_pb2(model.to_pb2()) == model


# ---------------------------------------------------------------------------
# leaf builders, bottom-up
# ---------------------------------------------------------------------------


def _node_definition_pb2() -> registration_pb2.Registration.NodeDefinition:
    msg = R.NodeDefinition(node_type=R.NodeType.NODE_TYPE_RADAR)
    msg.node_sub_type.extend(["long-range", "tracking"])
    return msg


def _node_definition_model() -> NodeDefinition:
    return NodeDefinition(
        node_type=R.NodeType.NODE_TYPE_RADAR,
        node_sub_type=["long-range", "tracking"],
    )


def _capability_pb2() -> registration_pb2.Registration.Capability:
    return R.Capability(
        category="Radar", type="Maximum Transmit Power", value="50", units="dB"
    )


def _capability_model() -> Capability:
    return Capability(
        category="Radar", type="Maximum Transmit Power", value="50", units="dB"
    )


def _duration_pb2(
    value: float = 5.0,
    units: registration_pb2.Registration.TimeUnits = (
        R.TimeUnits.TIME_UNITS_SECONDS
    ),
) -> registration_pb2.Registration.Duration:
    return R.Duration(units=units, value=value)


def _duration_model(
    value: float = 5.0,
    units: registration_pb2.Registration.TimeUnits = (
        R.TimeUnits.TIME_UNITS_SECONDS
    ),
) -> Duration:
    return Duration(units=units, value=value)


def _mode_parameter_pb2() -> registration_pb2.Registration.ModeParameter:
    return R.ModeParameter(type="SelfAdaptation", value="ROI")


def _mode_parameter_model() -> ModeParameter:
    return ModeParameter(type="SelfAdaptation", value="ROI")


def _location_type_location_pb2() -> registration_pb2.Registration.LocationType:
    return R.LocationType(
        location_units=(
            location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M
        ),
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        zone="30N",
    )


def _location_type_location_model() -> LocationType:
    return LocationType(
        location_units=(
            location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M
        ),
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        zone="30N",
    )


def _location_type_range_bearing_pb2() -> registration_pb2.Registration.LocationType:
    return R.LocationType(
        range_bearing_units=(
            range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M
        ),
        range_bearing_datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _location_type_range_bearing_model() -> LocationType:
    return LocationType(
        range_bearing_units=(
            range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M
        ),
        range_bearing_datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )


def _velocity_type_pb2() -> registration_pb2.Registration.VelocityType:
    msg = R.VelocityType(
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        zone="30N",
    )
    msg.enu_velocity_units.CopyFrom(
        velocity_pb2.ENUVelocityUnits(
            east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
        )
    )
    return msg


def _velocity_type_model() -> VelocityType:
    return VelocityType(
        enu_velocity_units=ENUVelocityUnits(
            east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
        ),
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        zone="30N",
    )


def _status_report_pb2() -> registration_pb2.Registration.StatusReport:
    return R.StatusReport(
        category=R.StatusReportCategory.STATUS_REPORT_CATEGORY_SENSOR,
        type="temperature",
        units="Celsius",
        on_change=True,
    )


def _status_report_model() -> StatusReport:
    return StatusReport(
        category=R.StatusReportCategory.STATUS_REPORT_CATEGORY_SENSOR,
        type="temperature",
        units="Celsius",
        on_change=True,
    )


def _performance_value_pb2() -> registration_pb2.Registration.PerformanceValue:
    return R.PerformanceValue(
        type="Rotation speed",
        units="Degrees per second",
        unit_value="2.5",
        variation_type="Linear",
    )


def _performance_value_model() -> PerformanceValue:
    return PerformanceValue(
        type="Rotation speed",
        units="Degrees per second",
        unit_value="2.5",
        variation_type="Linear",
    )


def _geometric_error_pb2() -> registration_pb2.Registration.GeometricError:
    msg = R.GeometricError(
        type="Standard Deviation", units="metres", variation_type="Linear with Range"
    )
    msg.performance_value.extend([_performance_value_pb2()])
    return msg


def _geometric_error_model() -> GeometricError:
    return GeometricError(
        type="Standard Deviation",
        units="metres",
        variation_type="Linear with Range",
        performance_value=[_performance_value_model()],
    )


def _detection_report_pb2() -> registration_pb2.Registration.DetectionReport:
    return R.DetectionReport(
        category=R.DetectionReportCategory.DETECTION_REPORT_CATEGORY_OBJECT,
        type="colour",
        units="Red, Green, Blue, Yellow",
        on_change=True,
    )


def _detection_report_model() -> DetectionReport:
    return DetectionReport(
        category=R.DetectionReportCategory.DETECTION_REPORT_CATEGORY_OBJECT,
        type="colour",
        units="Red, Green, Blue, Yellow",
        on_change=True,
    )


def _behaviour_definition_pb2() -> registration_pb2.Registration.BehaviourDefinition:
    return R.BehaviourDefinition(type="Loitering")


def _behaviour_definition_model() -> BehaviourDefinition:
    return BehaviourDefinition(type="Loitering")


def _sub_class_leaf_pb2() -> registration_pb2.Registration.SubClass:
    return R.SubClass(type="Car", level=1)


def _sub_class_leaf_model() -> SubClass:
    return SubClass(type="Car", level=1)


def _sub_class_pb2() -> registration_pb2.Registration.SubClass:
    msg = R.SubClass(type="Vehicle", level=0)
    msg.sub_class.extend([_sub_class_leaf_pb2()])
    return msg


def _sub_class_model() -> SubClass:
    return SubClass(type="Vehicle", level=0, sub_class=[_sub_class_leaf_model()])


def _class_definition_pb2() -> registration_pb2.Registration.ClassDefinition:
    msg = R.ClassDefinition(type="Vehicle", units="probability")
    msg.sub_class.extend([_sub_class_pb2()])
    return msg


def _class_definition_model() -> ClassDefinition:
    return ClassDefinition(
        type="Vehicle", units="probability", sub_class=[_sub_class_model()]
    )


def _extension_subclass_pb2() -> registration_pb2.Registration.ExtensionSubclass:
    return R.ExtensionSubclass(
        Subclass_namespace="urn:example:taxonomy",
        Subclass_name="Drone",
        units="probability",
    )


def _extension_subclass_model() -> ExtensionSubclass:
    return ExtensionSubclass(
        Subclass_namespace="urn:example:taxonomy",
        Subclass_name="Drone",
        units="probability",
    )


def _taxonomy_dock_definition_pb2() -> (
    registration_pb2.Registration.TaxonomyDockDefinition
):
    msg = R.TaxonomyDockDefinition(
        Dock_class_namespace="urn:example:base", Dock_class="Object"
    )
    msg.Extension_subclass.extend([_extension_subclass_pb2()])
    return msg


def _taxonomy_dock_definition_model() -> TaxonomyDockDefinition:
    return TaxonomyDockDefinition(
        Dock_class_namespace="urn:example:base",
        Dock_class="Object",
        Extension_subclass=[_extension_subclass_model()],
    )


def _detection_class_definition_pb2() -> (
    registration_pb2.Registration.DetectionClassDefinition
):
    msg = R.DetectionClassDefinition(
        confidence_definition=R.ConfidenceDefinition.CONFIDENCE_DEFINITION_MULTI_CLASS
    )
    msg.class_performance.extend([_performance_value_pb2()])
    msg.class_definition.extend([_class_definition_pb2()])
    msg.taxonomy_dock_definition.extend([_taxonomy_dock_definition_pb2()])
    return msg


def _detection_class_definition_model() -> DetectionClassDefinition:
    return DetectionClassDefinition(
        confidence_definition=R.ConfidenceDefinition.CONFIDENCE_DEFINITION_MULTI_CLASS,
        class_performance=[_performance_value_model()],
        class_definition=[_class_definition_model()],
        taxonomy_dock_definition=[_taxonomy_dock_definition_model()],
    )


def _detection_definition_pb2() -> registration_pb2.Registration.DetectionDefinition:
    msg = R.DetectionDefinition()
    msg.location_type.CopyFrom(_location_type_location_pb2())
    msg.detection_performance.extend([_performance_value_pb2()])
    msg.detection_report.extend([_detection_report_pb2()])
    msg.detection_class_definition.extend([_detection_class_definition_pb2()])
    msg.behaviour_definition.extend([_behaviour_definition_pb2()])
    msg.velocity_type.CopyFrom(_velocity_type_pb2())
    msg.geometric_error.CopyFrom(_geometric_error_pb2())
    return msg


def _detection_definition_model() -> DetectionDefinition:
    return DetectionDefinition(
        location_type=_location_type_location_model(),
        detection_performance=[_performance_value_model()],
        detection_report=[_detection_report_model()],
        detection_class_definition=[_detection_class_definition_model()],
        behaviour_definition=[_behaviour_definition_model()],
        velocity_type=_velocity_type_model(),
        geometric_error=_geometric_error_model(),
    )


def _filter_parameter_pb2() -> registration_pb2.Registration.FilterParameter:
    msg = R.FilterParameter(parameter="speed")
    msg.operators.extend([registration_pb2.Operator.OPERATOR_GREATER_THAN])
    return msg


def _filter_parameter_model() -> FilterParameter:
    return FilterParameter(
        parameter="speed",
        operators=[registration_pb2.Operator.OPERATOR_GREATER_THAN],
    )


def _sub_class_filter_definition_leaf_pb2() -> (
    registration_pb2.Registration.SubClassFilterDefinition
):
    msg = R.SubClassFilterDefinition(level=1, type="Car")
    msg.filter_parameter.extend([_filter_parameter_pb2()])
    return msg


def _sub_class_filter_definition_leaf_model() -> SubClassFilterDefinition:
    return SubClassFilterDefinition(
        level=1, type="Car", filter_parameter=[_filter_parameter_model()]
    )


def _sub_class_filter_definition_pb2() -> (
    registration_pb2.Registration.SubClassFilterDefinition
):
    msg = R.SubClassFilterDefinition(level=0, type="Vehicle")
    msg.sub_class_definition.extend([_sub_class_filter_definition_leaf_pb2()])
    return msg


def _sub_class_filter_definition_model() -> SubClassFilterDefinition:
    return SubClassFilterDefinition(
        level=0,
        type="Vehicle",
        sub_class_definition=[_sub_class_filter_definition_leaf_model()],
    )


def _class_filter_definition_pb2() -> (
    registration_pb2.Registration.ClassFilterDefinition
):
    msg = R.ClassFilterDefinition(type="Vehicle")
    msg.filter_parameter.extend([_filter_parameter_pb2()])
    msg.sub_class_definition.extend([_sub_class_filter_definition_pb2()])
    return msg


def _class_filter_definition_model() -> ClassFilterDefinition:
    return ClassFilterDefinition(
        type="Vehicle",
        filter_parameter=[_filter_parameter_model()],
        sub_class_definition=[_sub_class_filter_definition_model()],
    )


def _behaviour_filter_definition_pb2() -> (
    registration_pb2.Registration.BehaviourFilterDefinition
):
    msg = R.BehaviourFilterDefinition(type="Loitering")
    msg.filter_parameter.extend([_filter_parameter_pb2()])
    return msg


def _behaviour_filter_definition_model() -> BehaviourFilterDefinition:
    return BehaviourFilterDefinition(
        type="Loitering", filter_parameter=[_filter_parameter_model()]
    )


def _command_pb2() -> registration_pb2.Registration.Command:
    msg = R.Command(units="degrees", type=R.CommandType.COMMAND_TYPE_LOOK_AT)
    msg.completion_time.CopyFrom(
        _duration_pb2(value=2.0, units=R.TimeUnits.TIME_UNITS_SECONDS)
    )
    return msg


def _command_model() -> Command:
    return Command(
        units="degrees",
        completion_time=_duration_model(
            value=2.0, units=R.TimeUnits.TIME_UNITS_SECONDS
        ),
        type=R.CommandType.COMMAND_TYPE_LOOK_AT,
    )


def _region_definition_pb2() -> registration_pb2.Registration.RegionDefinition:
    msg = R.RegionDefinition()
    msg.region_type.extend([R.RegionType.REGION_TYPE_AREA_OF_INTEREST])
    msg.settle_time.CopyFrom(
        _duration_pb2(value=1.0, units=R.TimeUnits.TIME_UNITS_SECONDS)
    )
    msg.region_area.extend([_location_type_location_pb2()])
    msg.class_filter_definition.extend([_class_filter_definition_pb2()])
    msg.behaviour_filter_definition.extend([_behaviour_filter_definition_pb2()])
    return msg


def _region_definition_model() -> RegionDefinition:
    return RegionDefinition(
        region_type=[R.RegionType.REGION_TYPE_AREA_OF_INTEREST],
        settle_time=_duration_model(value=1.0, units=R.TimeUnits.TIME_UNITS_SECONDS),
        region_area=[_location_type_location_model()],
        class_filter_definition=[_class_filter_definition_model()],
        behaviour_filter_definition=[_behaviour_filter_definition_model()],
    )


def _task_definition_pb2() -> registration_pb2.Registration.TaskDefinition:
    msg = R.TaskDefinition(concurrent_tasks=2)
    msg.region_definition.CopyFrom(_region_definition_pb2())
    msg.command.extend([_command_pb2()])
    return msg


def _task_definition_model() -> TaskDefinition:
    return TaskDefinition(
        concurrent_tasks=2,
        region_definition=_region_definition_model(),
        command=[_command_model()],
    )


def _mode_definition_pb2() -> registration_pb2.Registration.ModeDefinition:
    msg = R.ModeDefinition(
        mode_name="Search",
        mode_type=R.ModeType.MODE_TYPE_PERMANENT,
        mode_description="Wide area search",
        scan_type=R.ScanType.SCAN_TYPE_SCANNING,
        tracking_type=R.TrackingType.TRACKING_TYPE_TRACK,
    )
    msg.settle_time.CopyFrom(
        _duration_pb2(value=5.0, units=R.TimeUnits.TIME_UNITS_SECONDS)
    )
    msg.maximum_latency.CopyFrom(
        _duration_pb2(value=100.0, units=R.TimeUnits.TIME_UNITS_MILLISECONDS)
    )
    msg.duration.CopyFrom(
        _duration_pb2(value=10.0, units=R.TimeUnits.TIME_UNITS_MINUTES)
    )
    msg.mode_parameter.extend([_mode_parameter_pb2()])
    msg.detection_definition.extend([_detection_definition_pb2()])
    msg.task.CopyFrom(_task_definition_pb2())
    return msg


def _mode_definition_model() -> ModeDefinition:
    return ModeDefinition(
        mode_name="Search",
        mode_type=R.ModeType.MODE_TYPE_PERMANENT,
        mode_description="Wide area search",
        settle_time=_duration_model(value=5.0, units=R.TimeUnits.TIME_UNITS_SECONDS),
        maximum_latency=_duration_model(
            value=100.0, units=R.TimeUnits.TIME_UNITS_MILLISECONDS
        ),
        scan_type=R.ScanType.SCAN_TYPE_SCANNING,
        tracking_type=R.TrackingType.TRACKING_TYPE_TRACK,
        duration=_duration_model(value=10.0, units=R.TimeUnits.TIME_UNITS_MINUTES),
        mode_parameter=[_mode_parameter_model()],
        detection_definition=[_detection_definition_model()],
        task=_task_definition_model(),
    )


def _status_definition_pb2() -> registration_pb2.Registration.StatusDefinition:
    msg = R.StatusDefinition()
    msg.status_interval.CopyFrom(
        _duration_pb2(value=30.0, units=R.TimeUnits.TIME_UNITS_SECONDS)
    )
    msg.location_definition.CopyFrom(_location_type_location_pb2())
    msg.coverage_definition.CopyFrom(_location_type_range_bearing_pb2())
    msg.obscuration_definition.CopyFrom(_location_type_range_bearing_pb2())
    msg.status_report.extend([_status_report_pb2()])
    msg.field_of_view_definition.CopyFrom(_location_type_range_bearing_pb2())
    return msg


def _status_definition_model() -> StatusDefinition:
    return StatusDefinition(
        status_interval=_duration_model(
            value=30.0, units=R.TimeUnits.TIME_UNITS_SECONDS
        ),
        location_definition=_location_type_location_model(),
        coverage_definition=_location_type_range_bearing_model(),
        obscuration_definition=_location_type_range_bearing_model(),
        status_report=[_status_report_model()],
        field_of_view_definition=_location_type_range_bearing_model(),
    )


def _config_data_sub_pb2() -> registration_pb2.Registration.ConfigurationData:
    return R.ConfigurationData(manufacturer="Acme", model="Widget-100")


def _config_data_sub_model() -> ConfigurationData:
    return ConfigurationData(manufacturer="Acme", model="Widget-100")


def _config_data_pb2() -> registration_pb2.Registration.ConfigurationData:
    msg = R.ConfigurationData(
        manufacturer="Acme Corp",
        model="Widget-9000",
        serial_number="SN123",
        hardware_version="1.0",
        software_version="2.3.1",
    )
    msg.sub_components.extend([_config_data_sub_pb2()])
    return msg


def _config_data_model() -> ConfigurationData:
    return ConfigurationData(
        manufacturer="Acme Corp",
        model="Widget-9000",
        serial_number="SN123",
        hardware_version="1.0",
        software_version="2.3.1",
        sub_components=[_config_data_sub_model()],
    )


def _reporting_region_pb2() -> range_bearing_pb2.LocationOrRangeBearing:
    msg = range_bearing_pb2.LocationOrRangeBearing()
    msg.range_bearing.CopyFrom(
        range_bearing_pb2.RangeBearingCone(
            elevation=1.0,
            azimuth=2.0,
            range=3.0,
            coordinate_system=(
                range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M
            ),
            datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
        )
    )
    return msg


def _reporting_region_model() -> LocationOrRangeBearing:
    return LocationOrRangeBearing(
        range_bearing=RangeBearingCone(
            elevation=1.0,
            azimuth=2.0,
            range=3.0,
            coordinate_system=(
                range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M
            ),
            datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
        )
    )


def _registration_pb2() -> registration_pb2.Registration:
    msg = registration_pb2.Registration(
        icd_version=ICD_VERSION, name="Node One", short_name="N1"
    )
    msg.node_definition.extend([_node_definition_pb2()])
    msg.capabilities.extend([_capability_pb2()])
    msg.status_definition.CopyFrom(_status_definition_pb2())
    msg.mode_definition.extend([_mode_definition_pb2()])
    msg.dependent_nodes.extend(["node-2", "node-3"])
    msg.reporting_region.extend([_reporting_region_pb2()])
    msg.config_data.extend([_config_data_pb2()])
    return msg


def _registration_model() -> Registration:
    return Registration(
        node_definition=[_node_definition_model()],
        icd_version=ICD_VERSION,
        name="Node One",
        short_name="N1",
        capabilities=[_capability_model()],
        status_definition=_status_definition_model(),
        mode_definition=[_mode_definition_model()],
        dependent_nodes=["node-2", "node-3"],
        reporting_region=[_reporting_region_model()],
        config_data=[_config_data_model()],
    )


def _registration_ack_pb2() -> registration_ack_pb2.RegistrationAck:
    msg = registration_ack_pb2.RegistrationAck(acceptance=False)
    msg.ack_response_reason.extend(["missing capabilities", "bad icd_version"])
    return msg


def _registration_ack_model() -> RegistrationAck:
    return RegistrationAck(
        acceptance=False,
        ack_response_reason=["missing capabilities", "bad icd_version"],
    )


# ---------------------------------------------------------------------------
# round-trip tests: one per nested model, plus Registration/RegistrationAck
# ---------------------------------------------------------------------------


def test_node_definition_roundtrip() -> None:
    _assert_roundtrip(NodeDefinition, _node_definition_model, _node_definition_pb2)


def test_node_definition_unset_node_type_stays_unset() -> None:
    model = _node_definition_model().model_copy(update={"node_type": None})
    with pytest.raises(IcdValidationError, match="node_type"):
        model.to_pb2()


def test_capability_roundtrip() -> None:
    _assert_roundtrip(Capability, _capability_model, _capability_pb2)


def test_capability_unset_value_and_units_stay_unset() -> None:
    model = _capability_model().model_copy(update={"value": None, "units": None})
    pb = model.to_pb2()
    assert not pb.HasField("value")
    assert not pb.HasField("units")
    roundtripped = Capability.from_pb2(pb)
    assert roundtripped.value is None
    assert roundtripped.units is None


def test_duration_roundtrip() -> None:
    _assert_roundtrip(Duration, _duration_model, _duration_pb2)


def test_duration_requires_units_and_value() -> None:
    with pytest.raises(IcdValidationError, match="value"):
        Duration(units=R.TimeUnits.TIME_UNITS_SECONDS).to_pb2()


def test_mode_parameter_roundtrip() -> None:
    _assert_roundtrip(ModeParameter, _mode_parameter_model, _mode_parameter_pb2)


def test_mode_parameter_requires_type_and_value() -> None:
    with pytest.raises(IcdValidationError, match="value"):
        ModeParameter(type="SelfAdaptation").to_pb2()


def test_location_type_location_leg_roundtrip() -> None:
    _assert_roundtrip(
        LocationType, _location_type_location_model, _location_type_location_pb2
    )


def test_location_type_range_bearing_leg_roundtrip() -> None:
    _assert_roundtrip(
        LocationType,
        _location_type_range_bearing_model,
        _location_type_range_bearing_pb2,
    )


def test_location_type_zone_stays_unset() -> None:
    model = _location_type_location_model().model_copy(update={"zone": None})
    pb = model.to_pb2()
    assert not pb.HasField("zone")
    assert LocationType.from_pb2(pb).zone is None


def test_location_type_requires_exactly_one_coordinate_system() -> None:
    # Neither `coordinates_oneof` member set -> mandatory-oneof rejection.
    model = LocationType(
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E
    )
    with pytest.raises(IcdValidationError, match="coordinates_oneof"):
        model.to_pb2()


def test_location_type_rejects_both_coordinate_system_members_set() -> None:
    # Pydantic has no structural oneof enforcement -- both `coordinates_oneof`
    # members (`location_units` AND `range_bearing_units`, per
    # `LocationType.DESCRIPTOR.oneofs_by_name["coordinates_oneof"]`) CAN be
    # set simultaneously at construction; only `_require_mandatory()`'s
    # `len(set_members) != 1` check at `to_pb2()` guards against that.
    # `datum_oneof` is left with a single valid member (`location_datum`) so
    # the rejection is isolated to `coordinates_oneof`.
    model = LocationType(
        location_units=(
            location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M
        ),
        range_bearing_units=(
            range_bearing_pb2.RangeBearingCoordinateSystem.RANGE_BEARING_COORDINATE_SYSTEM_DEGREES_M
        ),
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )
    with pytest.raises(IcdValidationError, match="coordinates_oneof"):
        model.to_pb2()


def test_velocity_type_roundtrip() -> None:
    _assert_roundtrip(VelocityType, _velocity_type_model, _velocity_type_pb2)


def test_velocity_type_requires_velocity_units() -> None:
    # `velocity_units_oneof` (only `enu_velocity_units` live) is mandatory.
    model = VelocityType(
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E
    )
    with pytest.raises(IcdValidationError, match="velocity_units_oneof"):
        model.to_pb2()


def test_velocity_type_rejects_both_datum_members_set() -> None:
    # `velocity_units_oneof` has only one live member (`enu_velocity_units`
    # -- the other three historical members are `reserved` in the .proto),
    # so it structurally cannot exercise a "both members set" case. Its
    # sibling mandatory oneof, `datum_oneof` (per
    # `VelocityType.DESCRIPTOR.oneofs_by_name["datum_oneof"]`), has two
    # members -- `location_datum` AND `range_bearing_datum` -- and pydantic
    # again allows both to be set at construction; only
    # `_require_mandatory()`'s `len(set_members) != 1` check at `to_pb2()`
    # rejects it. `velocity_units_oneof` is left satisfied (single valid
    # member set) so the rejection is isolated to `datum_oneof`.
    model = VelocityType(
        enu_velocity_units=ENUVelocityUnits(
            east_north_rate_units=velocity_pb2.SpeedUnits.SPEED_UNITS_MS,
        ),
        location_datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
        range_bearing_datum=range_bearing_pb2.RangeBearingDatum.RANGE_BEARING_DATUM_TRUE,
    )
    with pytest.raises(IcdValidationError, match="datum_oneof"):
        model.to_pb2()


def test_status_report_roundtrip() -> None:
    _assert_roundtrip(StatusReport, _status_report_model, _status_report_pb2)


def test_status_report_unset_on_change_stays_unset() -> None:
    model = _status_report_model().model_copy(update={"on_change": None})
    pb = model.to_pb2()
    assert not pb.HasField("on_change")
    assert StatusReport.from_pb2(pb).on_change is None


def test_performance_value_roundtrip() -> None:
    _assert_roundtrip(
        PerformanceValue, _performance_value_model, _performance_value_pb2
    )


def test_performance_value_unset_variation_type_stays_unset() -> None:
    model = _performance_value_model().model_copy(update={"variation_type": None})
    pb = model.to_pb2()
    assert not pb.HasField("variation_type")
    assert PerformanceValue.from_pb2(pb).variation_type is None


def test_geometric_error_roundtrip() -> None:
    _assert_roundtrip(GeometricError, _geometric_error_model, _geometric_error_pb2)


def test_geometric_error_unset_performance_value_stays_empty() -> None:
    model = _geometric_error_model().model_copy(update={"performance_value": []})
    pb = model.to_pb2()
    assert list(pb.performance_value) == []
    assert GeometricError.from_pb2(pb).performance_value == []


def test_detection_report_roundtrip() -> None:
    _assert_roundtrip(DetectionReport, _detection_report_model, _detection_report_pb2)


def test_detection_report_unset_on_change_stays_unset() -> None:
    model = _detection_report_model().model_copy(update={"on_change": None})
    pb = model.to_pb2()
    assert not pb.HasField("on_change")
    assert DetectionReport.from_pb2(pb).on_change is None


def test_behaviour_definition_roundtrip() -> None:
    _assert_roundtrip(
        BehaviourDefinition, _behaviour_definition_model, _behaviour_definition_pb2
    )


def test_behaviour_definition_unset_units_stays_unset() -> None:
    model = _behaviour_definition_model().model_copy(update={"units": None})
    pb = model.to_pb2()
    assert not pb.HasField("units")
    assert BehaviourDefinition.from_pb2(pb).units is None


def test_sub_class_recursive_roundtrip() -> None:
    _assert_roundtrip(SubClass, _sub_class_model, _sub_class_pb2)


def test_sub_class_unset_sub_class_stays_empty() -> None:
    model = _sub_class_model().model_copy(update={"sub_class": []})
    pb = model.to_pb2()
    assert list(pb.sub_class) == []
    assert SubClass.from_pb2(pb).sub_class == []


def test_class_definition_roundtrip() -> None:
    _assert_roundtrip(ClassDefinition, _class_definition_model, _class_definition_pb2)


def test_class_definition_unset_units_stays_unset() -> None:
    model = _class_definition_model().model_copy(update={"units": None})
    pb = model.to_pb2()
    assert not pb.HasField("units")
    assert ClassDefinition.from_pb2(pb).units is None


def test_extension_subclass_roundtrip() -> None:
    _assert_roundtrip(
        ExtensionSubclass, _extension_subclass_model, _extension_subclass_pb2
    )


def test_extension_subclass_unset_units_stays_unset() -> None:
    model = _extension_subclass_model().model_copy(update={"units": None})
    pb = model.to_pb2()
    assert not pb.HasField("units")
    assert ExtensionSubclass.from_pb2(pb).units is None


def test_taxonomy_dock_definition_roundtrip() -> None:
    _assert_roundtrip(
        TaxonomyDockDefinition,
        _taxonomy_dock_definition_model,
        _taxonomy_dock_definition_pb2,
    )


def test_taxonomy_dock_definition_unset_extension_subclass_stays_empty() -> None:
    model = _taxonomy_dock_definition_model().model_copy(
        update={"Extension_subclass": []}
    )
    pb = model.to_pb2()
    assert list(pb.Extension_subclass) == []
    assert TaxonomyDockDefinition.from_pb2(pb).Extension_subclass == []


def test_detection_class_definition_roundtrip() -> None:
    _assert_roundtrip(
        DetectionClassDefinition,
        _detection_class_definition_model,
        _detection_class_definition_pb2,
    )


def test_detection_class_definition_unset_confidence_definition_stays_unset() -> None:
    model = _detection_class_definition_model().model_copy(
        update={"confidence_definition": None}
    )
    pb = model.to_pb2()
    assert not pb.HasField("confidence_definition")
    assert DetectionClassDefinition.from_pb2(pb).confidence_definition is None


def test_detection_definition_roundtrip() -> None:
    _assert_roundtrip(
        DetectionDefinition, _detection_definition_model, _detection_definition_pb2
    )


def test_detection_definition_unset_velocity_type_stays_unset() -> None:
    model = _detection_definition_model().model_copy(update={"velocity_type": None})
    pb = model.to_pb2()
    assert not pb.HasField("velocity_type")
    assert DetectionDefinition.from_pb2(pb).velocity_type is None


def test_filter_parameter_roundtrip() -> None:
    _assert_roundtrip(FilterParameter, _filter_parameter_model, _filter_parameter_pb2)


def test_filter_parameter_requires_parameter_and_operators() -> None:
    with pytest.raises(IcdValidationError, match="operators"):
        FilterParameter(parameter="speed").to_pb2()


def test_sub_class_filter_definition_recursive_roundtrip() -> None:
    _assert_roundtrip(
        SubClassFilterDefinition,
        _sub_class_filter_definition_model,
        _sub_class_filter_definition_pb2,
    )


def test_sub_class_filter_definition_unset_filter_parameter_stays_empty() -> None:
    model = _sub_class_filter_definition_leaf_model().model_copy(
        update={"filter_parameter": []}
    )
    pb = model.to_pb2()
    assert list(pb.filter_parameter) == []
    assert SubClassFilterDefinition.from_pb2(pb).filter_parameter == []


def test_class_filter_definition_roundtrip() -> None:
    _assert_roundtrip(
        ClassFilterDefinition,
        _class_filter_definition_model,
        _class_filter_definition_pb2,
    )


def test_class_filter_definition_unset_sub_class_definition_stays_empty() -> None:
    model = _class_filter_definition_model().model_copy(
        update={"sub_class_definition": []}
    )
    pb = model.to_pb2()
    assert list(pb.sub_class_definition) == []
    assert ClassFilterDefinition.from_pb2(pb).sub_class_definition == []


def test_behaviour_filter_definition_roundtrip() -> None:
    _assert_roundtrip(
        BehaviourFilterDefinition,
        _behaviour_filter_definition_model,
        _behaviour_filter_definition_pb2,
    )


def test_behaviour_filter_definition_unset_filter_parameter_stays_empty() -> None:
    model = _behaviour_filter_definition_model().model_copy(
        update={"filter_parameter": []}
    )
    pb = model.to_pb2()
    assert list(pb.filter_parameter) == []
    assert BehaviourFilterDefinition.from_pb2(pb).filter_parameter == []


def test_command_roundtrip() -> None:
    _assert_roundtrip(Command, _command_model, _command_pb2)


def test_command_requires_units_completion_time_and_type() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        Command(
            units="degrees",
            completion_time=_duration_model(
                value=2.0, units=R.TimeUnits.TIME_UNITS_SECONDS
            ),
        ).to_pb2()


def test_region_definition_roundtrip() -> None:
    _assert_roundtrip(
        RegionDefinition, _region_definition_model, _region_definition_pb2
    )


def test_region_definition_unset_settle_time_stays_unset() -> None:
    model = _region_definition_model().model_copy(update={"settle_time": None})
    pb = model.to_pb2()
    assert not pb.HasField("settle_time")
    assert RegionDefinition.from_pb2(pb).settle_time is None


def test_task_definition_roundtrip() -> None:
    _assert_roundtrip(TaskDefinition, _task_definition_model, _task_definition_pb2)


def test_task_definition_unset_concurrent_tasks_stays_unset() -> None:
    model = _task_definition_model().model_copy(update={"concurrent_tasks": None})
    pb = model.to_pb2()
    assert not pb.HasField("concurrent_tasks")
    assert TaskDefinition.from_pb2(pb).concurrent_tasks is None


def test_mode_definition_roundtrip() -> None:
    _assert_roundtrip(ModeDefinition, _mode_definition_model, _mode_definition_pb2)


def test_mode_definition_unset_mode_description_stays_unset() -> None:
    model = _mode_definition_model().model_copy(update={"mode_description": None})
    pb = model.to_pb2()
    assert not pb.HasField("mode_description")
    assert ModeDefinition.from_pb2(pb).mode_description is None


def test_status_definition_roundtrip() -> None:
    _assert_roundtrip(
        StatusDefinition, _status_definition_model, _status_definition_pb2
    )


def test_status_definition_unset_location_definition_stays_unset() -> None:
    model = _status_definition_model().model_copy(update={"location_definition": None})
    pb = model.to_pb2()
    assert not pb.HasField("location_definition")
    assert StatusDefinition.from_pb2(pb).location_definition is None


def test_configuration_data_recursive_roundtrip() -> None:
    _assert_roundtrip(ConfigurationData, _config_data_model, _config_data_pb2)


def test_configuration_data_unset_serial_number_stays_unset() -> None:
    model = _config_data_model().model_copy(update={"serial_number": None})
    pb = model.to_pb2()
    assert not pb.HasField("serial_number")
    assert ConfigurationData.from_pb2(pb).serial_number is None


def test_configuration_data_requires_non_empty_manufacturer_and_model() -> None:
    # manufacturer/model are presence-less mandatory (plain `string` fields,
    # no `optional` keyword) -- same shape as follow.FollowObject.
    # follow_object_id (Task 4): default "" must still be rejected.
    with pytest.raises(IcdValidationError, match="manufacturer"):
        ConfigurationData(model="Widget-9000").to_pb2()


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_registration_to_pb2_matches_native() -> None:
    assert _registration_model().to_pb2() == _registration_pb2()


def test_registration_from_pb2_matches_native() -> None:
    assert Registration.from_pb2(_registration_pb2()) == _registration_model()


def test_registration_double_roundtrip() -> None:
    model = _registration_model()
    assert Registration.from_pb2(model.to_pb2()) == model


def test_registration_unset_name_and_short_name_stay_unset() -> None:
    model = _registration_model().model_copy(update={"name": None, "short_name": None})
    pb = model.to_pb2()
    assert not pb.HasField("name")
    assert not pb.HasField("short_name")
    roundtripped = Registration.from_pb2(pb)
    assert roundtripped.name is None
    assert roundtripped.short_name is None


def test_registration_icd_version_defaults_to_module_constant() -> None:
    assert Registration().icd_version == ICD_VERSION == "BSI Flex 335 v2.0"


def test_registration_dependent_nodes_and_reporting_region_are_optional() -> None:
    model = _registration_model().model_copy(
        update={"dependent_nodes": [], "reporting_region": []}
    )
    pb = model.to_pb2()
    assert list(pb.dependent_nodes) == []
    assert list(pb.reporting_region) == []
    roundtripped = Registration.from_pb2(pb)
    assert roundtripped.dependent_nodes == []
    assert roundtripped.reporting_region == []


# ---------------------------------------------------------------------------
# Registration mandatory-field validation (IcdValidationError)
# ---------------------------------------------------------------------------


def test_registration_to_pb2_lists_all_mandatory_fields_when_empty() -> None:
    with pytest.raises(IcdValidationError) as excinfo:
        Registration(icd_version=None).to_pb2()
    message = str(excinfo.value)
    for field_name in (
        "node_definition",
        "icd_version",
        "capabilities",
        "status_definition",
        "mode_definition",
        "config_data",
    ):
        assert field_name in message


def test_registration_from_pb2_lists_all_mandatory_fields_on_empty_pb2() -> None:
    with pytest.raises(IcdValidationError) as excinfo:
        Registration.from_pb2(registration_pb2.Registration())
    message = str(excinfo.value)
    for field_name in (
        "node_definition",
        "icd_version",
        "capabilities",
        "status_definition",
        "mode_definition",
        "config_data",
    ):
        assert field_name in message


# ---------------------------------------------------------------------------
# registration_ack.RegistrationAck
# ---------------------------------------------------------------------------


def test_registration_ack_to_pb2_matches_native() -> None:
    assert _registration_ack_model().to_pb2() == _registration_ack_pb2()


def test_registration_ack_from_pb2_matches_native() -> None:
    assert (
        RegistrationAck.from_pb2(_registration_ack_pb2())
        == _registration_ack_model()
    )


def test_registration_ack_double_roundtrip() -> None:
    model = _registration_ack_model()
    assert RegistrationAck.from_pb2(model.to_pb2()) == model


def test_registration_ack_unset_ack_response_reason_stays_empty() -> None:
    pb = RegistrationAck(acceptance=True).to_pb2()
    assert list(pb.ack_response_reason) == []
    assert RegistrationAck.from_pb2(pb).ack_response_reason == []


def test_registration_ack_requires_acceptance() -> None:
    with pytest.raises(IcdValidationError, match="acceptance"):
        RegistrationAck(ack_response_reason=["x"]).to_pb2()
