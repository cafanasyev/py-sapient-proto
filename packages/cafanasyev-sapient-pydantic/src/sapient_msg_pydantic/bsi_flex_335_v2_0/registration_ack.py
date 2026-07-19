"""Pydantic models for registration_ack.proto."""
from __future__ import annotations

from typing import ClassVar

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import registration_ack_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel


class RegistrationAck(SapientModel):
    pb2_cls: ClassVar = registration_ack_pb2.RegistrationAck

    acceptance: bool | None = None
    ack_response_reason: list[str] = Field(default_factory=list)

    def to_pb2(self) -> registration_ack_pb2.RegistrationAck:
        self._require_mandatory()
        msg = registration_ack_pb2.RegistrationAck()
        if self.acceptance is not None:
            msg.acceptance = self.acceptance
        msg.ack_response_reason.extend(self.ack_response_reason)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_ack_pb2.RegistrationAck) -> Self:
        model = cls(
            acceptance=msg.acceptance if msg.HasField("acceptance") else None,
            ack_response_reason=list(msg.ack_response_reason),
        )
        model._require_mandatory()
        return model
