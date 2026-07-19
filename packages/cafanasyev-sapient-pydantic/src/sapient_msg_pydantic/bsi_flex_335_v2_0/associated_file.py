"""Pydantic models for associated_file.proto."""
from __future__ import annotations

from typing import ClassVar

from sapient_msg.bsi_flex_335_v2_0 import associated_file_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel


class AssociatedFile(SapientModel):
    pb2_cls: ClassVar = associated_file_pb2.AssociatedFile

    type: str | None = None
    url: str | None = None

    def to_pb2(self) -> associated_file_pb2.AssociatedFile:
        self._require_mandatory()
        msg = associated_file_pb2.AssociatedFile()
        if self.type is not None:
            msg.type = self.type
        if self.url is not None:
            msg.url = self.url
        return msg

    @classmethod
    def from_pb2(cls, msg: associated_file_pb2.AssociatedFile) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            url=msg.url if msg.HasField("url") else None,
        )
        model._require_mandatory()
        return model
