"""Pydantic models for location.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import location_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    LocationCoordinateSystem: TypeAlias = (
        location_pb2.LocationCoordinateSystem
    )
    LocationDatum: TypeAlias = location_pb2.LocationDatum
else:
    LocationCoordinateSystem = int
    LocationDatum = int


class Location(SapientModel):
    pb2_cls: ClassVar = location_pb2.Location

    # All fields are `optional` in the .proto; mandatory ones are enforced
    # only at to_pb2() by `_require_mandatory()`.
    x: float | None = None
    y: float | None = None
    z: float | None = None
    x_error: float | None = None
    y_error: float | None = None
    z_error: float | None = None
    coordinate_system: LocationCoordinateSystem | None = None
    datum: LocationDatum | None = None
    utm_zone: str | None = None

    def to_pb2(self) -> location_pb2.Location:
        self._require_mandatory()
        msg = location_pb2.Location()
        if self.x is not None:
            msg.x = self.x
        if self.y is not None:
            msg.y = self.y
        if self.z is not None:
            msg.z = self.z
        if self.x_error is not None:
            msg.x_error = self.x_error
        if self.y_error is not None:
            msg.y_error = self.y_error
        if self.z_error is not None:
            msg.z_error = self.z_error
        if self.coordinate_system is not None:
            msg.coordinate_system = self.coordinate_system
        if self.datum is not None:
            msg.datum = self.datum
        if self.utm_zone is not None:
            msg.utm_zone = self.utm_zone
        return msg

    @classmethod
    def from_pb2(cls, msg: location_pb2.Location) -> Self:
        model = cls(
            x=msg.x if msg.HasField("x") else None,
            y=msg.y if msg.HasField("y") else None,
            z=msg.z if msg.HasField("z") else None,
            x_error=msg.x_error if msg.HasField("x_error") else None,
            y_error=msg.y_error if msg.HasField("y_error") else None,
            z_error=msg.z_error if msg.HasField("z_error") else None,
            coordinate_system=(
                msg.coordinate_system if msg.HasField("coordinate_system") else None
            ),
            datum=msg.datum if msg.HasField("datum") else None,
            utm_zone=msg.utm_zone if msg.HasField("utm_zone") else None,
        )
        model._require_mandatory()
        return model


class LocationList(SapientModel):
    pb2_cls: ClassVar = location_pb2.LocationList

    locations: list[Location] = Field(default_factory=list)

    def to_pb2(self) -> location_pb2.LocationList:
        self._require_mandatory()
        msg = location_pb2.LocationList()
        msg.locations.extend(x.to_pb2() for x in self.locations)
        return msg

    @classmethod
    def from_pb2(cls, msg: location_pb2.LocationList) -> Self:
        model = cls(locations=[Location.from_pb2(x) for x in msg.locations])
        model._require_mandatory()
        return model
