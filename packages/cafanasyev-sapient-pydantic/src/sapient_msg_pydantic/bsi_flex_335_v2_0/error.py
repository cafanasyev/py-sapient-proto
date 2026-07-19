"""Pydantic models for error.proto."""
from __future__ import annotations

from typing import ClassVar

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import error_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel


class Error(SapientModel):
    pb2_cls: ClassVar = error_pb2.Error

    packet: bytes | None = None
    error_message: list[str] = Field(default_factory=list)

    def to_pb2(self) -> error_pb2.Error:
        self._require_mandatory()
        msg = error_pb2.Error()
        if self.packet is not None:
            msg.packet = self.packet
        msg.error_message.extend(self.error_message)
        return msg

    @classmethod
    def from_pb2(cls, msg: error_pb2.Error) -> Self:
        model = cls(
            packet=msg.packet if msg.HasField("packet") else None,
            error_message=list(msg.error_message),
        )
        model._require_mandatory()
        return model
