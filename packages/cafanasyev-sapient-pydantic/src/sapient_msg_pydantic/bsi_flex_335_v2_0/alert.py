"""Pydantic models for alert.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import alert_pb2
from typing_extensions import Self
from ulid import ULID

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_detection import (
    AssociatedDetection,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.associated_file import AssociatedFile
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import Location
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import RangeBearing

if TYPE_CHECKING:
    AlertType: TypeAlias = alert_pb2.Alert.AlertType
    AlertStatus: TypeAlias = alert_pb2.Alert.AlertStatus
    DiscretePriority: TypeAlias = alert_pb2.Alert.DiscretePriority
else:
    AlertType = int
    AlertStatus = int
    DiscretePriority = int


class Alert(SapientModel):
    pb2_cls: ClassVar = alert_pb2.Alert

    # alert_id is minted by this message -> fresh ULID default; region_id
    alert_id: str | None = Field(default_factory=lambda: str(ULID()))
    alert_type: AlertType | None = None
    status: AlertStatus | None = None
    description: str | None = None
    # location_oneof (not mandatory): range_bearing | location.
    range_bearing: RangeBearing | None = None
    location: Location | None = None
    region_id: str | None = None
    priority: DiscretePriority | None = None
    ranking: float | None = None
    confidence: float | None = None
    associated_file: list[AssociatedFile] = Field(default_factory=list)
    associated_detection: list[AssociatedDetection] = Field(default_factory=list)
    additional_information: str | None = None

    def to_pb2(self) -> alert_pb2.Alert:
        self._require_mandatory()
        msg = alert_pb2.Alert()
        if self.alert_id is not None:
            msg.alert_id = self.alert_id
        if self.alert_type is not None:
            msg.alert_type = self.alert_type
        if self.status is not None:
            msg.status = self.status
        if self.description is not None:
            msg.description = self.description
        if self.range_bearing is not None:
            msg.range_bearing.CopyFrom(self.range_bearing.to_pb2())
        if self.location is not None:
            msg.location.CopyFrom(self.location.to_pb2())
        if self.region_id is not None:
            msg.region_id = self.region_id
        if self.priority is not None:
            msg.priority = self.priority
        if self.ranking is not None:
            msg.ranking = self.ranking
        if self.confidence is not None:
            msg.confidence = self.confidence
        msg.associated_file.extend(x.to_pb2() for x in self.associated_file)
        msg.associated_detection.extend(
            x.to_pb2() for x in self.associated_detection
        )
        if self.additional_information is not None:
            msg.additional_information = self.additional_information
        return msg

    @classmethod
    def from_pb2(cls, msg: alert_pb2.Alert) -> Self:
        model = cls(
            alert_id=msg.alert_id if msg.HasField("alert_id") else None,
            alert_type=msg.alert_type if msg.HasField("alert_type") else None,
            status=msg.status if msg.HasField("status") else None,
            description=msg.description if msg.HasField("description") else None,
            range_bearing=(
                RangeBearing.from_pb2(msg.range_bearing)
                if msg.HasField("range_bearing")
                else None
            ),
            location=(
                Location.from_pb2(msg.location) if msg.HasField("location") else None
            ),
            region_id=msg.region_id if msg.HasField("region_id") else None,
            priority=msg.priority if msg.HasField("priority") else None,
            ranking=msg.ranking if msg.HasField("ranking") else None,
            confidence=msg.confidence if msg.HasField("confidence") else None,
            associated_file=[AssociatedFile.from_pb2(x) for x in msg.associated_file],
            associated_detection=[
                AssociatedDetection.from_pb2(x) for x in msg.associated_detection
            ],
            additional_information=(
                msg.additional_information
                if msg.HasField("additional_information")
                else None
            ),
        )
        model._require_mandatory()
        return model
