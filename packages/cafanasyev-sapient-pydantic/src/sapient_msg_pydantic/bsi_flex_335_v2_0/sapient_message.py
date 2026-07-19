"""Pydantic model for sapient_message.proto: the top-level envelope."""
from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from sapient_msg.bsi_flex_335_v2_0 import sapient_message_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic._options import datetime_to_pb2, pb2_to_datetime
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert import Alert
from sapient_msg_pydantic.bsi_flex_335_v2_0.alert_ack import AlertAck
from sapient_msg_pydantic.bsi_flex_335_v2_0.detection_report import DetectionReport
from sapient_msg_pydantic.bsi_flex_335_v2_0.error import Error
from sapient_msg_pydantic.bsi_flex_335_v2_0.registration import Registration
from sapient_msg_pydantic.bsi_flex_335_v2_0.registration_ack import RegistrationAck
from sapient_msg_pydantic.bsi_flex_335_v2_0.status_report import StatusReport
from sapient_msg_pydantic.bsi_flex_335_v2_0.task import Task
from sapient_msg_pydantic.bsi_flex_335_v2_0.task_ack import TaskAck


class SapientMessage(SapientModel):
    pb2_cls: ClassVar = sapient_message_pb2.SapientMessage

    timestamp: datetime | None = None
    node_id: str | None = None
    destination_id: str | None = None

    # `content` oneof members (mandatory: exactly one must be set).
    registration: Registration | None = None
    registration_ack: RegistrationAck | None = None
    status_report: StatusReport | None = None
    detection_report: DetectionReport | None = None
    task: Task | None = None
    task_ack: TaskAck | None = None
    alert: Alert | None = None
    alert_ack: AlertAck | None = None
    error: Error | None = None

    additional_information: str | None = None

    def to_pb2(self) -> sapient_message_pb2.SapientMessage:
        self._require_mandatory()
        msg = sapient_message_pb2.SapientMessage()
        if self.timestamp is not None:
            msg.timestamp.CopyFrom(datetime_to_pb2(self.timestamp))
        if self.node_id is not None:
            msg.node_id = self.node_id
        if self.destination_id is not None:
            msg.destination_id = self.destination_id
        if self.additional_information is not None:
            msg.additional_information = self.additional_information

        if self.registration is not None:
            msg.registration.CopyFrom(self.registration.to_pb2())
        if self.registration_ack is not None:
            msg.registration_ack.CopyFrom(self.registration_ack.to_pb2())
        if self.status_report is not None:
            msg.status_report.CopyFrom(self.status_report.to_pb2())
        if self.detection_report is not None:
            msg.detection_report.CopyFrom(self.detection_report.to_pb2())
        if self.task is not None:
            msg.task.CopyFrom(self.task.to_pb2())
        if self.task_ack is not None:
            msg.task_ack.CopyFrom(self.task_ack.to_pb2())
        if self.alert is not None:
            msg.alert.CopyFrom(self.alert.to_pb2())
        if self.alert_ack is not None:
            msg.alert_ack.CopyFrom(self.alert_ack.to_pb2())
        if self.error is not None:
            msg.error.CopyFrom(self.error.to_pb2())

        return msg

    @classmethod
    def from_pb2(cls, msg: sapient_message_pb2.SapientMessage) -> Self:
        which_content = msg.WhichOneof("content")

        model = cls(
            timestamp=(
                pb2_to_datetime(msg.timestamp)
                if msg.HasField("timestamp")
                else None
            ),
            node_id=msg.node_id if msg.HasField("node_id") else None,
            destination_id=(
                msg.destination_id if msg.HasField("destination_id") else None
            ),
            registration=(
                Registration.from_pb2(msg.registration)
                if which_content == "registration"
                else None
            ),
            registration_ack=(
                RegistrationAck.from_pb2(msg.registration_ack)
                if which_content == "registration_ack"
                else None
            ),
            status_report=(
                StatusReport.from_pb2(msg.status_report)
                if which_content == "status_report"
                else None
            ),
            detection_report=(
                DetectionReport.from_pb2(msg.detection_report)
                if which_content == "detection_report"
                else None
            ),
            task=(
                Task.from_pb2(msg.task) if which_content == "task" else None
            ),
            task_ack=(
                TaskAck.from_pb2(msg.task_ack)
                if which_content == "task_ack"
                else None
            ),
            alert=(
                Alert.from_pb2(msg.alert) if which_content == "alert" else None
            ),
            alert_ack=(
                AlertAck.from_pb2(msg.alert_ack)
                if which_content == "alert_ack"
                else None
            ),
            error=(
                Error.from_pb2(msg.error) if which_content == "error" else None
            ),
            additional_information=(
                msg.additional_information
                if msg.HasField("additional_information")
                else None
            ),
        )
        model._require_mandatory()
        return model
