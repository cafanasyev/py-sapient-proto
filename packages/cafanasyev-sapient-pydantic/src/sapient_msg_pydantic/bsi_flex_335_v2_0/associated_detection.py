"""Pydantic models for associated_detection.proto."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, TypeAlias

from sapient_msg.bsi_flex_335_v2_0 import associated_detection_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic._options import datetime_to_pb2, pb2_to_datetime

if TYPE_CHECKING:
    AssociationRelation: TypeAlias = (
        associated_detection_pb2.AssociationRelation
    )
else:
    AssociationRelation = int


class AssociatedDetection(SapientModel):
    pb2_cls: ClassVar = associated_detection_pb2.AssociatedDetection

    timestamp: datetime | None = None
    node_id: str | None = None
    object_id: str | None = None
    association_type: AssociationRelation | None = None

    def to_pb2(self) -> associated_detection_pb2.AssociatedDetection:
        self._require_mandatory()
        msg = associated_detection_pb2.AssociatedDetection()
        if self.timestamp is not None:
            msg.timestamp.CopyFrom(datetime_to_pb2(self.timestamp))
        if self.node_id is not None:
            msg.node_id = self.node_id
        if self.object_id is not None:
            msg.object_id = self.object_id
        if self.association_type is not None:
            msg.association_type = self.association_type
        return msg

    @classmethod
    def from_pb2(cls, msg: associated_detection_pb2.AssociatedDetection) -> Self:
        model = cls(
            timestamp=(
                pb2_to_datetime(msg.timestamp) if msg.HasField("timestamp") else None
            ),
            node_id=msg.node_id if msg.HasField("node_id") else None,
            object_id=msg.object_id if msg.HasField("object_id") else None,
            association_type=(
                msg.association_type if msg.HasField("association_type") else None
            ),
        )
        model._require_mandatory()
        return model
