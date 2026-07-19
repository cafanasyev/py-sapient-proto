"""Pydantic models for alert_ack.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import alert_ack_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel

if TYPE_CHECKING:
    AlertAckStatus: TypeAlias = alert_ack_pb2.AlertAck.AlertAckStatus
else:
    AlertAckStatus = int


class AlertAck(SapientModel):
    pb2_cls: ClassVar = alert_ack_pb2.AlertAck

    alert_id: str | None = None
    reason: list[str] = Field(default_factory=list)
    alert_ack_status: AlertAckStatus | None = None

    def to_pb2(self) -> alert_ack_pb2.AlertAck:
        self._require_mandatory()
        msg = alert_ack_pb2.AlertAck()
        if self.alert_id is not None:
            msg.alert_id = self.alert_id
        msg.reason.extend(self.reason)
        if self.alert_ack_status is not None:
            msg.alert_ack_status = self.alert_ack_status
        return msg

    @classmethod
    def from_pb2(cls, msg: alert_ack_pb2.AlertAck) -> Self:
        model = cls(
            alert_id=msg.alert_id if msg.HasField("alert_id") else None,
            reason=list(msg.reason),
            alert_ack_status=(
                msg.alert_ack_status if msg.HasField("alert_ack_status") else None
            ),
        )
        model._require_mandatory()
        return model
