"""Pydantic models for follow.proto."""
from __future__ import annotations

from typing import ClassVar

from sapient_msg.bsi_flex_335_v2_0 import follow_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel


class FollowObject(SapientModel):
    pb2_cls: ClassVar = follow_pb2.FollowObject

    # follow_object_id lacks `optional` in the .proto (no presence):
    # proto-default "", direct assignment.
    follow_object_id: str = ""

    def to_pb2(self) -> follow_pb2.FollowObject:
        self._require_mandatory()
        msg = follow_pb2.FollowObject()
        msg.follow_object_id = self.follow_object_id
        return msg

    @classmethod
    def from_pb2(cls, msg: follow_pb2.FollowObject) -> Self:
        model = cls(follow_object_id=msg.follow_object_id)
        model._require_mandatory()
        return model
