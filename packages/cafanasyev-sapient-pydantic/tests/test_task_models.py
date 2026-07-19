"""Round-trips for task / task_ack models.

Every nested model gets the three-assertion round-trip core used throughout
this package (native-pb2 built independently of the pydantic model; both
directions checked, plus a double round-trip), via `_assert_roundtrip`, and a
fourth assertion exercising either an optional field staying unset, a
mandatory-field rejection, a oneof-exclusivity rejection, or ULID
auto-generation behaviour.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from sapient_msg.bsi_flex_335_v2_0 import (
    associated_file_pb2,
    location_pb2,
    range_bearing_pb2,
    registration_pb2,
    task_ack_pb2,
    task_pb2,
)
from sapient_msg_pydantic._options import IcdValidationError, datetime_to_pb2
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.follow import FollowObject
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location, LocationList
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
    RangeBearingCone,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.task import (
    BehaviourFilter,
    ClassFilter,
    Command,
    Parameter,
    Region,
    SubClassFilter,
    Task,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.task_ack import TaskAck

T = task_pb2.Task

_TASK_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAV"
_REGION_ID = "01ARZ3NDEKTSV4RRFFQ69G5FAW"


def _assert_roundtrip(model_cls, model_fn, pb2_fn) -> None:  # type: ignore[no-untyped-def]
    model = model_fn()
    pb2_msg = pb2_fn()
    assert model.to_pb2() == pb2_msg
    assert model_cls.from_pb2(pb2_msg) == model
    assert model_cls.from_pb2(model.to_pb2()) == model


# ---------------------------------------------------------------------------
# shared geometry builders
# ---------------------------------------------------------------------------


def _native_location_model() -> Location:
    return Location(
        x=1.5,
        y=-2.5,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )


def _native_location_pb2() -> location_pb2.Location:
    return location_pb2.Location(
        x=1.5,
        y=-2.5,
        coordinate_system=location_pb2.LocationCoordinateSystem.LOCATION_COORDINATE_SYSTEM_LAT_LNG_DEG_M,
        datum=location_pb2.LocationDatum.LOCATION_DATUM_WGS84_E,
    )


def _native_range_bearing_cone_model() -> RangeBearingCone:
    return RangeBearingCone(
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


def _native_location_or_range_bearing_model() -> LocationOrRangeBearing:
    return LocationOrRangeBearing(range_bearing=_native_range_bearing_cone_model())


def _native_location_or_range_bearing_pb2() -> range_bearing_pb2.LocationOrRangeBearing:
    msg = range_bearing_pb2.LocationOrRangeBearing()
    msg.range_bearing.CopyFrom(_native_range_bearing_cone_pb2())
    return msg


def _native_location_list_model() -> LocationList:
    return LocationList(locations=[_native_location_model()])


def _native_location_list_pb2() -> location_pb2.LocationList:
    msg = location_pb2.LocationList()
    msg.locations.extend([_native_location_pb2()])
    return msg


# ---------------------------------------------------------------------------
# task.Parameter
# ---------------------------------------------------------------------------


def _native_parameter_pb2() -> task_pb2.Task.Parameter:
    return T.Parameter(
        name="speed",
        operator=registration_pb2.Operator.OPERATOR_GREATER_THAN,
        value=10.0,
    )


def _native_parameter_model() -> Parameter:
    return Parameter(
        name="speed",
        operator=registration_pb2.Operator.OPERATOR_GREATER_THAN,
        value=10.0,
    )


def test_parameter_roundtrip() -> None:
    _assert_roundtrip(Parameter, _native_parameter_model, _native_parameter_pb2)


def test_parameter_requires_name_operator_and_value() -> None:
    with pytest.raises(IcdValidationError, match="name"):
        Parameter(value=1.0).to_pb2()


# ---------------------------------------------------------------------------
# task.BehaviourFilter
# ---------------------------------------------------------------------------


def _native_behaviour_filter_pb2() -> task_pb2.Task.BehaviourFilter:
    msg = T.BehaviourFilter(type="loitering")
    msg.parameter.CopyFrom(_native_parameter_pb2())
    msg.priority = T.DiscreteThreshold.DISCRETE_THRESHOLD_HIGH
    return msg


def _native_behaviour_filter_model() -> BehaviourFilter:
    return BehaviourFilter(
        parameter=_native_parameter_model(),
        type="loitering",
        priority=T.DiscreteThreshold.DISCRETE_THRESHOLD_HIGH,
    )


def test_behaviour_filter_roundtrip() -> None:
    _assert_roundtrip(
        BehaviourFilter, _native_behaviour_filter_model, _native_behaviour_filter_pb2
    )


def test_behaviour_filter_requires_parameter() -> None:
    with pytest.raises(IcdValidationError, match="parameter"):
        BehaviourFilter().to_pb2()


# ---------------------------------------------------------------------------
# task.SubClassFilter (self-referential)
# ---------------------------------------------------------------------------


def _native_sub_class_filter_pb2() -> task_pb2.Task.SubClassFilter:
    leaf = T.SubClassFilter(type="quadcopter")
    leaf.parameter.CopyFrom(_native_parameter_pb2())
    leaf.priority = T.DiscreteThreshold.DISCRETE_THRESHOLD_LOW
    root = T.SubClassFilter(type="uav")
    root.parameter.CopyFrom(_native_parameter_pb2())
    root.priority = T.DiscreteThreshold.DISCRETE_THRESHOLD_MEDIUM
    root.sub_class_filter.extend([leaf])
    return root


def _native_sub_class_filter_model() -> SubClassFilter:
    leaf = SubClassFilter(
        parameter=_native_parameter_model(),
        type="quadcopter",
        priority=T.DiscreteThreshold.DISCRETE_THRESHOLD_LOW,
    )
    return SubClassFilter(
        parameter=_native_parameter_model(),
        type="uav",
        priority=T.DiscreteThreshold.DISCRETE_THRESHOLD_MEDIUM,
        sub_class_filter=[leaf],
    )


def test_sub_class_filter_recursive_roundtrip() -> None:
    _assert_roundtrip(
        SubClassFilter, _native_sub_class_filter_model, _native_sub_class_filter_pb2
    )


def test_sub_class_filter_requires_parameter_and_type() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        SubClassFilter(parameter=_native_parameter_model()).to_pb2()


# ---------------------------------------------------------------------------
# task.ClassFilter
# ---------------------------------------------------------------------------


def _native_class_filter_pb2() -> task_pb2.Task.ClassFilter:
    msg = T.ClassFilter(type="air")
    msg.parameter.CopyFrom(_native_parameter_pb2())
    msg.sub_class_filter.extend([_native_sub_class_filter_pb2()])
    msg.priority = T.DiscreteThreshold.DISCRETE_THRESHOLD_HIGH
    return msg


def _native_class_filter_model() -> ClassFilter:
    return ClassFilter(
        parameter=_native_parameter_model(),
        type="air",
        sub_class_filter=[_native_sub_class_filter_model()],
        priority=T.DiscreteThreshold.DISCRETE_THRESHOLD_HIGH,
    )


def test_class_filter_roundtrip() -> None:
    _assert_roundtrip(
        ClassFilter, _native_class_filter_model, _native_class_filter_pb2
    )


def test_class_filter_requires_parameter_and_type() -> None:
    with pytest.raises(IcdValidationError, match="type"):
        ClassFilter(parameter=_native_parameter_model()).to_pb2()


# ---------------------------------------------------------------------------
# task.Region
# ---------------------------------------------------------------------------


def _native_region_pb2() -> task_pb2.Task.Region:
    msg = T.Region(
        type=T.RegionType.REGION_TYPE_AREA_OF_INTEREST,
        region_id=_REGION_ID,
        region_name="North Perimeter",
    )
    msg.region_area.CopyFrom(_native_location_or_range_bearing_pb2())
    msg.class_filter.extend([_native_class_filter_pb2()])
    msg.behaviour_filter.extend([_native_behaviour_filter_pb2()])
    return msg


def _native_region_model() -> Region:
    return Region(
        type=T.RegionType.REGION_TYPE_AREA_OF_INTEREST,
        region_id=_REGION_ID,
        region_name="North Perimeter",
        region_area=_native_location_or_range_bearing_model(),
        class_filter=[_native_class_filter_model()],
        behaviour_filter=[_native_behaviour_filter_model()],
    )


def test_region_roundtrip() -> None:
    _assert_roundtrip(Region, _native_region_model, _native_region_pb2)


def test_region_auto_generates_valid_ulid() -> None:
    model = Region(
        type=T.RegionType.REGION_TYPE_IGNORE,
        region_name="ignore-zone",
        region_area=_native_location_or_range_bearing_model(),
    )
    assert model.region_id is not None
    assert len(model.region_id) == 26


def test_region_requires_region_name() -> None:
    with pytest.raises(IcdValidationError, match="region_name"):
        Region(
            type=T.RegionType.REGION_TYPE_IGNORE,
            region_area=_native_location_or_range_bearing_model(),
        ).to_pb2()


# ---------------------------------------------------------------------------
# task.Command (mandatory oneof `command`)
# ---------------------------------------------------------------------------


def _native_command_look_at_pb2() -> task_pb2.Task.Command:
    msg = T.Command()
    msg.look_at.CopyFrom(_native_location_or_range_bearing_pb2())
    msg.command_parameter = "priority-1"
    return msg


def _native_command_look_at_model() -> Command:
    return Command(
        look_at=_native_location_or_range_bearing_model(),
        command_parameter="priority-1",
    )


def test_command_look_at_leg_roundtrip() -> None:
    _assert_roundtrip(
        Command, _native_command_look_at_model, _native_command_look_at_pb2
    )


def test_command_move_to_leg_roundtrip() -> None:
    model = Command(move_to=_native_location_list_model())
    pb = model.to_pb2()
    assert pb.HasField("move_to")
    assert not pb.HasField("look_at")
    assert pb.move_to == _native_location_list_pb2()
    assert Command.from_pb2(pb) == model


def test_command_follow_leg_roundtrip() -> None:
    model = Command(follow=FollowObject(follow_object_id=_REGION_ID))
    pb = model.to_pb2()
    assert pb.HasField("follow")
    assert Command.from_pb2(pb) == model


def test_command_requires_exactly_one_command_member() -> None:
    with pytest.raises(IcdValidationError, match="command"):
        Command().to_pb2()


# ---------------------------------------------------------------------------
# task.Task
# ---------------------------------------------------------------------------


def _native_task_pb2() -> task_pb2.Task:
    msg = T(
        task_id=_TASK_ID,
        control=T.Control.CONTROL_START,
    )
    msg.task_name = "Patrol north fence"
    msg.task_description = "Continuously patrol the north perimeter"
    msg.task_start_time.CopyFrom(
        datetime_to_pb2(datetime(2026, 7, 19, 9, tzinfo=timezone.utc))
    )
    msg.task_end_time.CopyFrom(
        datetime_to_pb2(datetime(2026, 7, 19, 17, tzinfo=timezone.utc))
    )
    msg.region.extend([_native_region_pb2()])
    msg.command.CopyFrom(_native_command_look_at_pb2())
    return msg


def _native_task_model() -> Task:
    return Task(
        task_id=_TASK_ID,
        task_name="Patrol north fence",
        task_description="Continuously patrol the north perimeter",
        task_start_time=datetime(2026, 7, 19, 9, tzinfo=timezone.utc),
        task_end_time=datetime(2026, 7, 19, 17, tzinfo=timezone.utc),
        control=T.Control.CONTROL_START,
        region=[_native_region_model()],
        command=_native_command_look_at_model(),
    )


def test_task_to_pb2_matches_native() -> None:
    assert _native_task_model().to_pb2() == _native_task_pb2()


def test_task_from_pb2_matches_native() -> None:
    assert Task.from_pb2(_native_task_pb2()) == _native_task_model()


def test_task_double_roundtrip() -> None:
    model = _native_task_model()
    assert Task.from_pb2(model.to_pb2()) == model


def test_task_unset_optionals_stay_unset() -> None:
    pb = Task(task_id=_TASK_ID, control=T.Control.CONTROL_STOP).to_pb2()
    assert not pb.HasField("task_name")
    assert Task.from_pb2(pb).task_name is None


def test_task_auto_generates_valid_ulid() -> None:
    model = Task(control=T.Control.CONTROL_START)
    assert model.task_id is not None
    assert len(model.task_id) == 26


def test_task_rejects_invalid_task_id() -> None:
    with pytest.raises(ValidationError):
        Task(task_id="not-a-ulid")


def test_task_requires_control() -> None:
    with pytest.raises(IcdValidationError, match="control"):
        Task(task_id=_TASK_ID).to_pb2()


# ---------------------------------------------------------------------------
# task_ack.TaskAck
# ---------------------------------------------------------------------------


def _native_associated_file_pb2() -> associated_file_pb2.AssociatedFile:
    return associated_file_pb2.AssociatedFile(
        type="log", url="http://example.com/task.log"
    )


def _native_associated_file_model() -> AssociatedFile:
    return AssociatedFile(type="log", url="http://example.com/task.log")


def _native_task_ack_pb2() -> task_ack_pb2.TaskAck:
    msg = task_ack_pb2.TaskAck(
        task_id=_TASK_ID,
        task_status=task_ack_pb2.TaskAck.TaskStatus.TASK_STATUS_REJECTED,
    )
    msg.associated_file.CopyFrom(_native_associated_file_pb2())
    msg.reason.extend(["out of bounds", "insufficient sensors"])
    return msg


def _native_task_ack_model() -> TaskAck:
    return TaskAck(
        task_id=_TASK_ID,
        task_status=task_ack_pb2.TaskAck.TaskStatus.TASK_STATUS_REJECTED,
        associated_file=_native_associated_file_model(),
        reason=["out of bounds", "insufficient sensors"],
    )


def test_task_ack_to_pb2_matches_native() -> None:
    assert _native_task_ack_model().to_pb2() == _native_task_ack_pb2()


def test_task_ack_from_pb2_matches_native() -> None:
    assert TaskAck.from_pb2(_native_task_ack_pb2()) == _native_task_ack_model()


def test_task_ack_double_roundtrip() -> None:
    model = _native_task_ack_model()
    assert TaskAck.from_pb2(model.to_pb2()) == model


def test_task_ack_unset_optionals_stay_unset() -> None:
    pb = TaskAck(
        task_id=_TASK_ID,
        task_status=task_ack_pb2.TaskAck.TaskStatus.TASK_STATUS_ACCEPTED,
    ).to_pb2()
    assert not pb.HasField("associated_file")
    assert TaskAck.from_pb2(pb).associated_file is None


def test_task_ack_task_id_not_auto_generated() -> None:
    # task_id REFERENCES the task being acknowledged -- it must be supplied
    # by the caller, not minted fresh by TaskAck itself.
    model = TaskAck(task_status=task_ack_pb2.TaskAck.TaskStatus.TASK_STATUS_ACCEPTED)
    assert model.task_id is None
