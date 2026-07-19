"""Pydantic models for task_ack.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import task_ack_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile

if TYPE_CHECKING:
    TaskStatus: TypeAlias = task_ack_pb2.TaskAck.TaskStatus
else:
    TaskStatus = int


class TaskAck(SapientModel):
    pb2_cls: ClassVar = task_ack_pb2.TaskAck

    task_id: str | None = None
    task_status: TaskStatus | None = None
    associated_file: AssociatedFile | None = None
    reason: list[str] = Field(default_factory=list)

    def to_pb2(self) -> task_ack_pb2.TaskAck:
        self._require_mandatory()
        msg = task_ack_pb2.TaskAck()
        if self.task_id is not None:
            msg.task_id = self.task_id
        if self.task_status is not None:
            msg.task_status = self.task_status
        if self.associated_file is not None:
            msg.associated_file.CopyFrom(self.associated_file.to_pb2())
        msg.reason.extend(self.reason)
        return msg

    @classmethod
    def from_pb2(cls, msg: task_ack_pb2.TaskAck) -> Self:
        model = cls(
            task_id=msg.task_id if msg.HasField("task_id") else None,
            task_status=(
                msg.task_status if msg.HasField("task_status") else None
            ),
            associated_file=(
                AssociatedFile.from_pb2(msg.associated_file)
                if msg.HasField("associated_file")
                else None
            ),
            reason=list(msg.reason),
        )
        model._require_mandatory()
        return model
