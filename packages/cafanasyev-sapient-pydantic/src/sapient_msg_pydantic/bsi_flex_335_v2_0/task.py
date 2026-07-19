"""Pydantic models for task.proto.

Every nested message declared inside `Task` in the .proto becomes a FLAT
top-level model here (e.g. `Task.Region` -> `Region`), matching the
`registration.py` convention.
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import registration_pb2, task_pb2
from typing_extensions import Self
from ulid import ULID

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic._options import datetime_to_pb2, pb2_to_datetime
from sapient_msg_pydantic.bsi_flex_335_v2_0.follow import FollowObject
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import LocationList
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
)

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    Control: TypeAlias = task_pb2.Task.Control
    DiscreteThreshold: TypeAlias = task_pb2.Task.DiscreteThreshold
    RegionType: TypeAlias = task_pb2.Task.RegionType
    # Operator is a top-level enum from registration.proto, so it is only
    # available via registration_pb2.
    Operator: TypeAlias = registration_pb2.Operator
else:
    Control = int
    DiscreteThreshold = int
    RegionType = int
    Operator = int


class Parameter(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task.Parameter

    name: str | None = None
    operator: Operator | None = None
    value: float | None = None

    def to_pb2(self) -> task_pb2.Task.Parameter:
        self._require_mandatory()
        msg = task_pb2.Task.Parameter()
        if self.name is not None:
            msg.name = self.name
        if self.operator is not None:
            msg.operator = self.operator
        if self.value is not None:
            msg.value = self.value
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.Parameter) -> Self:
        model = cls(
            name=msg.name if msg.HasField("name") else None,
            operator=msg.operator if msg.HasField("operator") else None,
            value=msg.value if msg.HasField("value") else None,
        )
        model._require_mandatory()
        return model


class BehaviourFilter(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task.BehaviourFilter

    parameter: Parameter | None = None
    type: str | None = None
    priority: DiscreteThreshold | None = None

    def to_pb2(self) -> task_pb2.Task.BehaviourFilter:
        self._require_mandatory()
        msg = task_pb2.Task.BehaviourFilter()
        if self.parameter is not None:
            msg.parameter.CopyFrom(self.parameter.to_pb2())
        if self.type is not None:
            msg.type = self.type
        if self.priority is not None:
            msg.priority = self.priority
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.BehaviourFilter) -> Self:
        model = cls(
            parameter=(
                Parameter.from_pb2(msg.parameter)
                if msg.HasField("parameter")
                else None
            ),
            type=msg.type if msg.HasField("type") else None,
            priority=msg.priority if msg.HasField("priority") else None,
        )
        model._require_mandatory()
        return model


class SubClassFilter(SapientModel):
    """Self-referential filter node: `sub_class_filter: List[SubClassFilter]`."""

    pb2_cls: ClassVar = task_pb2.Task.SubClassFilter

    parameter: Parameter | None = None
    type: str | None = None
    sub_class_filter: list[SubClassFilter] = Field(default_factory=list)
    priority: DiscreteThreshold | None = None

    def to_pb2(self) -> task_pb2.Task.SubClassFilter:
        self._require_mandatory()
        msg = task_pb2.Task.SubClassFilter()
        if self.parameter is not None:
            msg.parameter.CopyFrom(self.parameter.to_pb2())
        if self.type is not None:
            msg.type = self.type
        msg.sub_class_filter.extend(x.to_pb2() for x in self.sub_class_filter)
        if self.priority is not None:
            msg.priority = self.priority
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.SubClassFilter) -> Self:
        model = cls(
            parameter=(
                Parameter.from_pb2(msg.parameter)
                if msg.HasField("parameter")
                else None
            ),
            type=msg.type if msg.HasField("type") else None,
            sub_class_filter=[
                SubClassFilter.from_pb2(x) for x in msg.sub_class_filter
            ],
            priority=msg.priority if msg.HasField("priority") else None,
        )
        model._require_mandatory()
        return model


class ClassFilter(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task.ClassFilter

    parameter: Parameter | None = None
    type: str | None = None
    sub_class_filter: list[SubClassFilter] = Field(default_factory=list)
    priority: DiscreteThreshold | None = None

    def to_pb2(self) -> task_pb2.Task.ClassFilter:
        self._require_mandatory()
        msg = task_pb2.Task.ClassFilter()
        if self.parameter is not None:
            msg.parameter.CopyFrom(self.parameter.to_pb2())
        if self.type is not None:
            msg.type = self.type
        msg.sub_class_filter.extend(x.to_pb2() for x in self.sub_class_filter)
        if self.priority is not None:
            msg.priority = self.priority
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.ClassFilter) -> Self:
        model = cls(
            parameter=(
                Parameter.from_pb2(msg.parameter)
                if msg.HasField("parameter")
                else None
            ),
            type=msg.type if msg.HasField("type") else None,
            sub_class_filter=[
                SubClassFilter.from_pb2(x) for x in msg.sub_class_filter
            ],
            priority=msg.priority if msg.HasField("priority") else None,
        )
        model._require_mandatory()
        return model


class Region(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task.Region

    type: RegionType | None = None
    # region_id is minted by this message -> fresh ULID default.
    region_id: str | None = Field(default_factory=lambda: str(ULID()))
    region_name: str | None = None
    region_area: LocationOrRangeBearing | None = None
    class_filter: list[ClassFilter] = Field(default_factory=list)
    behaviour_filter: list[BehaviourFilter] = Field(default_factory=list)

    def to_pb2(self) -> task_pb2.Task.Region:
        self._require_mandatory()
        msg = task_pb2.Task.Region()
        if self.type is not None:
            msg.type = self.type
        if self.region_id is not None:
            msg.region_id = self.region_id
        if self.region_name is not None:
            msg.region_name = self.region_name
        if self.region_area is not None:
            msg.region_area.CopyFrom(self.region_area.to_pb2())
        msg.class_filter.extend(x.to_pb2() for x in self.class_filter)
        msg.behaviour_filter.extend(x.to_pb2() for x in self.behaviour_filter)
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.Region) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            region_id=msg.region_id if msg.HasField("region_id") else None,
            region_name=(
                msg.region_name if msg.HasField("region_name") else None
            ),
            region_area=(
                LocationOrRangeBearing.from_pb2(msg.region_area)
                if msg.HasField("region_area")
                else None
            ),
            class_filter=[ClassFilter.from_pb2(x) for x in msg.class_filter],
            behaviour_filter=[
                BehaviourFilter.from_pb2(x) for x in msg.behaviour_filter
            ],
        )
        model._require_mandatory()
        return model


class Command(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task.Command

    # `command` is a mandatory oneof with nine members; exactly one of these
    # must be set (enforced by `_require_mandatory()`'s oneof check).
    request: str | None = None
    detection_threshold: DiscreteThreshold | None = None
    detection_report_rate: DiscreteThreshold | None = None
    classification_threshold: DiscreteThreshold | None = None
    mode_change: str | None = None
    look_at: LocationOrRangeBearing | None = None
    move_to: LocationList | None = None
    patrol: LocationList | None = None
    follow: FollowObject | None = None
    command_parameter: str | None = None

    def to_pb2(self) -> task_pb2.Task.Command:
        self._require_mandatory()
        msg = task_pb2.Task.Command()
        if self.request is not None:
            msg.request = self.request
        if self.detection_threshold is not None:
            msg.detection_threshold = self.detection_threshold
        if self.detection_report_rate is not None:
            msg.detection_report_rate = self.detection_report_rate
        if self.classification_threshold is not None:
            msg.classification_threshold = self.classification_threshold
        if self.mode_change is not None:
            msg.mode_change = self.mode_change
        if self.look_at is not None:
            msg.look_at.CopyFrom(self.look_at.to_pb2())
        if self.move_to is not None:
            msg.move_to.CopyFrom(self.move_to.to_pb2())
        if self.patrol is not None:
            msg.patrol.CopyFrom(self.patrol.to_pb2())
        if self.follow is not None:
            msg.follow.CopyFrom(self.follow.to_pb2())
        if self.command_parameter is not None:
            msg.command_parameter = self.command_parameter
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task.Command) -> Self:
        model = cls(
            request=msg.request if msg.HasField("request") else None,
            detection_threshold=(
                msg.detection_threshold
                if msg.HasField("detection_threshold")
                else None
            ),
            detection_report_rate=(
                msg.detection_report_rate
                if msg.HasField("detection_report_rate")
                else None
            ),
            classification_threshold=(
                msg.classification_threshold
                if msg.HasField("classification_threshold")
                else None
            ),
            mode_change=msg.mode_change if msg.HasField("mode_change") else None,
            look_at=(
                LocationOrRangeBearing.from_pb2(msg.look_at)
                if msg.HasField("look_at")
                else None
            ),
            move_to=(
                LocationList.from_pb2(msg.move_to)
                if msg.HasField("move_to")
                else None
            ),
            patrol=(
                LocationList.from_pb2(msg.patrol)
                if msg.HasField("patrol")
                else None
            ),
            follow=(
                FollowObject.from_pb2(msg.follow)
                if msg.HasField("follow")
                else None
            ),
            command_parameter=(
                msg.command_parameter
                if msg.HasField("command_parameter")
                else None
            ),
        )
        model._require_mandatory()
        return model


class Task(SapientModel):
    pb2_cls: ClassVar = task_pb2.Task

    # task_id is minted by this message -> fresh ULID default.
    task_id: str | None = Field(default_factory=lambda: str(ULID()))
    task_name: str | None = None
    task_description: str | None = None
    task_start_time: datetime | None = None
    task_end_time: datetime | None = None
    control: Control | None = None
    region: list[Region] = Field(default_factory=list)
    command: Command | None = None

    def to_pb2(self) -> task_pb2.Task:
        self._require_mandatory()
        msg = task_pb2.Task()
        if self.task_id is not None:
            msg.task_id = self.task_id
        if self.task_name is not None:
            msg.task_name = self.task_name
        if self.task_description is not None:
            msg.task_description = self.task_description
        if self.task_start_time is not None:
            msg.task_start_time.CopyFrom(datetime_to_pb2(self.task_start_time))
        if self.task_end_time is not None:
            msg.task_end_time.CopyFrom(datetime_to_pb2(self.task_end_time))
        if self.control is not None:
            msg.control = self.control
        msg.region.extend(x.to_pb2() for x in self.region)
        if self.command is not None:
            msg.command.CopyFrom(self.command.to_pb2())
        return msg

    @classmethod
    def from_pb2(cls, msg: task_pb2.Task) -> Self:
        model = cls(
            task_id=msg.task_id if msg.HasField("task_id") else None,
            task_name=msg.task_name if msg.HasField("task_name") else None,
            task_description=(
                msg.task_description if msg.HasField("task_description") else None
            ),
            task_start_time=(
                pb2_to_datetime(msg.task_start_time)
                if msg.HasField("task_start_time")
                else None
            ),
            task_end_time=(
                pb2_to_datetime(msg.task_end_time)
                if msg.HasField("task_end_time")
                else None
            ),
            control=msg.control if msg.HasField("control") else None,
            region=[Region.from_pb2(x) for x in msg.region],
            command=(
                Command.from_pb2(msg.command) if msg.HasField("command") else None
            ),
        )
        model._require_mandatory()
        return model
