"""Pydantic models for detection_report.proto.

`DetectionReport.SubClass` (recursive: `sub_class: List["SubClass"]`) is this
message's OWN nested taxonomy type -- distinct from `registration.SubClass`,
which lives in a different module and is never imported here.
"""
from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import detection_report_pb2
from typing_extensions import Self
from ulid import ULID

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic._options import datetime_to_pb2, pb2_to_datetime
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_detection import (
    AssociatedDetection,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import RangeBearing
from sapient_msg_pydantic.bsi_flex_335_v2_0.velocity import ENUVelocity


class PredictedLocation(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.PredictedLocation

    # predicted_location_oneof (not mandatory): range_bearing | location.
    range_bearing: RangeBearing | None = None
    location: Location | None = None
    predicted_timestamp: datetime | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport.PredictedLocation:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.PredictedLocation()
        if self.range_bearing is not None:
            msg.range_bearing.CopyFrom(self.range_bearing.to_pb2())
        if self.location is not None:
            msg.location.CopyFrom(self.location.to_pb2())
        if self.predicted_timestamp is not None:
            msg.predicted_timestamp.CopyFrom(
                datetime_to_pb2(self.predicted_timestamp)
            )
        return msg

    @classmethod
    def from_pb2(
        cls, msg: detection_report_pb2.DetectionReport.PredictedLocation
    ) -> Self:
        model = cls(
            range_bearing=(
                RangeBearing.from_pb2(msg.range_bearing)
                if msg.HasField("range_bearing")
                else None
            ),
            location=(
                Location.from_pb2(msg.location)
                if msg.HasField("location")
                else None
            ),
            predicted_timestamp=(
                pb2_to_datetime(msg.predicted_timestamp)
                if msg.HasField("predicted_timestamp")
                else None
            ),
        )
        model._require_mandatory()
        return model


class TrackObjectInfo(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.TrackObjectInfo

    type: str | None = None
    value: str | None = None
    error: float | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport.TrackObjectInfo:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.TrackObjectInfo()
        if self.type is not None:
            msg.type = self.type
        if self.value is not None:
            msg.value = self.value
        if self.error is not None:
            msg.error = self.error
        return msg

    @classmethod
    def from_pb2(
        cls, msg: detection_report_pb2.DetectionReport.TrackObjectInfo
    ) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            value=msg.value if msg.HasField("value") else None,
            error=msg.error if msg.HasField("error") else None,
        )
        model._require_mandatory()
        return model


class SubClass(SapientModel):
    """DetectionReport's own self-referential taxonomy node.

    `sub_class: List[SubClass]` resolves fine under pydantic v2 without an
    explicit `model_rebuild()` (same precedent as `registration.SubClass`).
    """

    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.SubClass

    type: str | None = None
    confidence: float | None = None
    level: int | None = None
    sub_class: list[SubClass] = Field(default_factory=list)

    def to_pb2(self) -> detection_report_pb2.DetectionReport.SubClass:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.SubClass()
        if self.type is not None:
            msg.type = self.type
        if self.confidence is not None:
            msg.confidence = self.confidence
        if self.level is not None:
            msg.level = self.level
        msg.sub_class.extend(x.to_pb2() for x in self.sub_class)
        return msg

    @classmethod
    def from_pb2(cls, msg: detection_report_pb2.DetectionReport.SubClass) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            confidence=msg.confidence if msg.HasField("confidence") else None,
            level=msg.level if msg.HasField("level") else None,
            sub_class=[SubClass.from_pb2(x) for x in msg.sub_class],
        )
        model._require_mandatory()
        return model


class DetectionReportClassification(SapientModel):
    pb2_cls: ClassVar = (
        detection_report_pb2.DetectionReport.DetectionReportClassification
    )

    type: str | None = None
    confidence: float | None = None
    sub_class: list[SubClass] = Field(default_factory=list)

    def to_pb2(
        self,
    ) -> detection_report_pb2.DetectionReport.DetectionReportClassification:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.DetectionReportClassification()
        if self.type is not None:
            msg.type = self.type
        if self.confidence is not None:
            msg.confidence = self.confidence
        msg.sub_class.extend(x.to_pb2() for x in self.sub_class)
        return msg

    @classmethod
    def from_pb2(
        cls,
        msg: detection_report_pb2.DetectionReport.DetectionReportClassification,
    ) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            confidence=msg.confidence if msg.HasField("confidence") else None,
            sub_class=[SubClass.from_pb2(x) for x in msg.sub_class],
        )
        model._require_mandatory()
        return model


class Behaviour(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.Behaviour

    type: str | None = None
    confidence: float | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport.Behaviour:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.Behaviour()
        if self.type is not None:
            msg.type = self.type
        if self.confidence is not None:
            msg.confidence = self.confidence
        return msg

    @classmethod
    def from_pb2(cls, msg: detection_report_pb2.DetectionReport.Behaviour) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            confidence=msg.confidence if msg.HasField("confidence") else None,
        )
        model._require_mandatory()
        return model


class Signal(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.Signal

    amplitude: float | None = None
    start_frequency: float | None = None
    centre_frequency: float | None = None
    stop_frequency: float | None = None
    pulse_duration: float | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport.Signal:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.Signal()
        if self.amplitude is not None:
            msg.amplitude = self.amplitude
        if self.start_frequency is not None:
            msg.start_frequency = self.start_frequency
        if self.centre_frequency is not None:
            msg.centre_frequency = self.centre_frequency
        if self.stop_frequency is not None:
            msg.stop_frequency = self.stop_frequency
        if self.pulse_duration is not None:
            msg.pulse_duration = self.pulse_duration
        return msg

    @classmethod
    def from_pb2(cls, msg: detection_report_pb2.DetectionReport.Signal) -> Self:
        model = cls(
            amplitude=msg.amplitude if msg.HasField("amplitude") else None,
            start_frequency=(
                msg.start_frequency if msg.HasField("start_frequency") else None
            ),
            centre_frequency=(
                msg.centre_frequency if msg.HasField("centre_frequency") else None
            ),
            stop_frequency=(
                msg.stop_frequency if msg.HasField("stop_frequency") else None
            ),
            pulse_duration=(
                msg.pulse_duration if msg.HasField("pulse_duration") else None
            ),
        )
        model._require_mandatory()
        return model


class DerivedDetection(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport.DerivedDetection

    timestamp: datetime | None = None
    node_id: str | None = None
    object_id: str | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport.DerivedDetection:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport.DerivedDetection()
        if self.timestamp is not None:
            msg.timestamp.CopyFrom(datetime_to_pb2(self.timestamp))
        if self.node_id is not None:
            msg.node_id = self.node_id
        if self.object_id is not None:
            msg.object_id = self.object_id
        return msg

    @classmethod
    def from_pb2(
        cls, msg: detection_report_pb2.DetectionReport.DerivedDetection
    ) -> Self:
        model = cls(
            timestamp=(
                pb2_to_datetime(msg.timestamp) if msg.HasField("timestamp") else None
            ),
            node_id=msg.node_id if msg.HasField("node_id") else None,
            object_id=msg.object_id if msg.HasField("object_id") else None,
        )
        model._require_mandatory()
        return model


class DetectionReport(SapientModel):
    pb2_cls: ClassVar = detection_report_pb2.DetectionReport

    # report_id is minted by this message -> fresh ULID default; object_id
    report_id: str | None = Field(default_factory=lambda: str(ULID()))
    object_id: str | None = None
    task_id: str | None = None
    state: str | None = None
    # location_oneof (range_bearing | location) is a mandatory oneof.
    range_bearing: RangeBearing | None = None
    location: Location | None = None
    detection_confidence: float | None = None
    track_info: list[TrackObjectInfo] = Field(default_factory=list)
    prediction_location: PredictedLocation | None = None
    object_info: list[TrackObjectInfo] = Field(default_factory=list)
    classification: list[DetectionReportClassification] = Field(
        default_factory=list
    )
    behaviour: list[Behaviour] = Field(default_factory=list)
    associated_file: list[AssociatedFile] = Field(default_factory=list)
    signal: list[Signal] = Field(default_factory=list)
    associated_detection: list[AssociatedDetection] = Field(default_factory=list)
    derived_detection: list[DerivedDetection] = Field(default_factory=list)
    # velocity_oneof (not mandatory): only enu_velocity is live, rest reserved.
    enu_velocity: ENUVelocity | None = None
    colour: str | None = None
    id: str | None = None

    def to_pb2(self) -> detection_report_pb2.DetectionReport:
        self._require_mandatory()
        msg = detection_report_pb2.DetectionReport()
        if self.report_id is not None:
            msg.report_id = self.report_id
        if self.object_id is not None:
            msg.object_id = self.object_id
        if self.task_id is not None:
            msg.task_id = self.task_id
        if self.state is not None:
            msg.state = self.state
        if self.range_bearing is not None:
            msg.range_bearing.CopyFrom(self.range_bearing.to_pb2())
        if self.location is not None:
            msg.location.CopyFrom(self.location.to_pb2())
        if self.detection_confidence is not None:
            msg.detection_confidence = self.detection_confidence
        msg.track_info.extend(x.to_pb2() for x in self.track_info)
        if self.prediction_location is not None:
            msg.prediction_location.CopyFrom(self.prediction_location.to_pb2())
        msg.object_info.extend(x.to_pb2() for x in self.object_info)
        msg.classification.extend(x.to_pb2() for x in self.classification)
        msg.behaviour.extend(x.to_pb2() for x in self.behaviour)
        msg.associated_file.extend(x.to_pb2() for x in self.associated_file)
        msg.signal.extend(x.to_pb2() for x in self.signal)
        msg.associated_detection.extend(
            x.to_pb2() for x in self.associated_detection
        )
        msg.derived_detection.extend(x.to_pb2() for x in self.derived_detection)
        if self.enu_velocity is not None:
            msg.enu_velocity.CopyFrom(self.enu_velocity.to_pb2())
        if self.colour is not None:
            msg.colour = self.colour
        if self.id is not None:
            msg.id = self.id
        return msg

    @classmethod
    def from_pb2(cls, msg: detection_report_pb2.DetectionReport) -> Self:
        model = cls(
            report_id=msg.report_id if msg.HasField("report_id") else None,
            object_id=msg.object_id if msg.HasField("object_id") else None,
            task_id=msg.task_id if msg.HasField("task_id") else None,
            state=msg.state if msg.HasField("state") else None,
            range_bearing=(
                RangeBearing.from_pb2(msg.range_bearing)
                if msg.HasField("range_bearing")
                else None
            ),
            location=(
                Location.from_pb2(msg.location)
                if msg.HasField("location")
                else None
            ),
            detection_confidence=(
                msg.detection_confidence
                if msg.HasField("detection_confidence")
                else None
            ),
            track_info=[TrackObjectInfo.from_pb2(x) for x in msg.track_info],
            prediction_location=(
                PredictedLocation.from_pb2(msg.prediction_location)
                if msg.HasField("prediction_location")
                else None
            ),
            object_info=[TrackObjectInfo.from_pb2(x) for x in msg.object_info],
            classification=[
                DetectionReportClassification.from_pb2(x)
                for x in msg.classification
            ],
            behaviour=[Behaviour.from_pb2(x) for x in msg.behaviour],
            associated_file=[
                AssociatedFile.from_pb2(x) for x in msg.associated_file
            ],
            signal=[Signal.from_pb2(x) for x in msg.signal],
            associated_detection=[
                AssociatedDetection.from_pb2(x) for x in msg.associated_detection
            ],
            derived_detection=[
                DerivedDetection.from_pb2(x) for x in msg.derived_detection
            ],
            enu_velocity=(
                ENUVelocity.from_pb2(msg.enu_velocity)
                if msg.HasField("enu_velocity")
                else None
            ),
            colour=msg.colour if msg.HasField("colour") else None,
            id=msg.id if msg.HasField("id") else None,
        )
        model._require_mandatory()
        return model
