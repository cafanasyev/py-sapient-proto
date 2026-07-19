"""Pydantic models for status_report.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import status_report_pb2
from typing_extensions import Self
from ulid import ULID

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
)

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    System: TypeAlias = status_report_pb2.StatusReport.System
    PowerSource: TypeAlias = status_report_pb2.StatusReport.PowerSource
    PowerStatus: TypeAlias = status_report_pb2.StatusReport.PowerStatus
    Info: TypeAlias = status_report_pb2.StatusReport.Info
    StatusType: TypeAlias = status_report_pb2.StatusReport.StatusType
    StatusLevel: TypeAlias = status_report_pb2.StatusReport.StatusLevel
else:
    System = int
    PowerSource = int
    PowerStatus = int
    Info = int
    StatusType = int
    StatusLevel = int


class Power(SapientModel):
    pb2_cls: ClassVar = status_report_pb2.StatusReport.Power

    level: int | None = None
    # source/status lack `optional` in the .proto (no presence):
    # proto-default 0 == *_UNSPECIFIED, direct assignment.
    source: PowerSource = PowerSource(0)
    status: PowerStatus = PowerStatus(0)

    def to_pb2(self) -> status_report_pb2.StatusReport.Power:
        self._require_mandatory()
        msg = status_report_pb2.StatusReport.Power()
        if self.level is not None:
            msg.level = self.level
        msg.source = self.source
        msg.status = self.status
        return msg

    @classmethod
    def from_pb2(cls, msg: status_report_pb2.StatusReport.Power) -> Self:
        model = cls(
            level=msg.level if msg.HasField("level") else None,
            source=msg.source,
            status=msg.status,
        )
        model._require_mandatory()
        return model


class Status(SapientModel):
    pb2_cls: ClassVar = status_report_pb2.StatusReport.Status

    status_level: StatusLevel | None = None
    status_value: str | None = None
    status_type: StatusType | None = None

    def to_pb2(self) -> status_report_pb2.StatusReport.Status:
        self._require_mandatory()
        msg = status_report_pb2.StatusReport.Status()
        if self.status_level is not None:
            msg.status_level = self.status_level
        if self.status_value is not None:
            msg.status_value = self.status_value
        if self.status_type is not None:
            msg.status_type = self.status_type
        return msg

    @classmethod
    def from_pb2(cls, msg: status_report_pb2.StatusReport.Status) -> Self:
        model = cls(
            status_level=(
                msg.status_level if msg.HasField("status_level") else None
            ),
            status_value=(
                msg.status_value if msg.HasField("status_value") else None
            ),
            status_type=msg.status_type if msg.HasField("status_type") else None,
        )
        model._require_mandatory()
        return model


class StatusReport(SapientModel):
    pb2_cls: ClassVar = status_report_pb2.StatusReport

    # report_id is this message's own identity (is_mandatory, is_ulid) -> auto
    # -generate a fresh ULID by default. active_task_id is also is_ulid but
    # references an *existing* task the ASM is currently performing, so it
    # stays plain (matches Alert.alert_id vs region_id from Task 4/registration).
    report_id: str | None = Field(default_factory=lambda: str(ULID()))
    system: System | None = None
    info: Info | None = None
    active_task_id: str | None = None
    mode: str | None = None
    power: Power | None = None
    node_location: Location | None = None
    field_of_view: LocationOrRangeBearing | None = None
    obscuration: list[LocationOrRangeBearing] = Field(default_factory=list)
    status: list[Status] = Field(default_factory=list)
    coverage: list[LocationOrRangeBearing] = Field(default_factory=list)

    def to_pb2(self) -> status_report_pb2.StatusReport:
        self._require_mandatory()
        msg = status_report_pb2.StatusReport()
        if self.report_id is not None:
            msg.report_id = self.report_id
        if self.system is not None:
            msg.system = self.system
        if self.info is not None:
            msg.info = self.info
        if self.active_task_id is not None:
            msg.active_task_id = self.active_task_id
        if self.mode is not None:
            msg.mode = self.mode
        if self.power is not None:
            msg.power.CopyFrom(self.power.to_pb2())
        if self.node_location is not None:
            msg.node_location.CopyFrom(self.node_location.to_pb2())
        if self.field_of_view is not None:
            msg.field_of_view.CopyFrom(self.field_of_view.to_pb2())
        msg.obscuration.extend(x.to_pb2() for x in self.obscuration)
        msg.status.extend(x.to_pb2() for x in self.status)
        msg.coverage.extend(x.to_pb2() for x in self.coverage)
        return msg

    @classmethod
    def from_pb2(cls, msg: status_report_pb2.StatusReport) -> Self:
        model = cls(
            report_id=msg.report_id if msg.HasField("report_id") else None,
            system=msg.system if msg.HasField("system") else None,
            info=msg.info if msg.HasField("info") else None,
            active_task_id=(
                msg.active_task_id if msg.HasField("active_task_id") else None
            ),
            mode=msg.mode if msg.HasField("mode") else None,
            power=Power.from_pb2(msg.power) if msg.HasField("power") else None,
            node_location=(
                Location.from_pb2(msg.node_location)
                if msg.HasField("node_location")
                else None
            ),
            field_of_view=(
                LocationOrRangeBearing.from_pb2(msg.field_of_view)
                if msg.HasField("field_of_view")
                else None
            ),
            obscuration=[
                LocationOrRangeBearing.from_pb2(x) for x in msg.obscuration
            ],
            status=[Status.from_pb2(x) for x in msg.status],
            coverage=[LocationOrRangeBearing.from_pb2(x) for x in msg.coverage],
        )
        model._require_mandatory()
        return model
