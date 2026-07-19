"""Pydantic models for range_bearing.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from sapient_msg.bsi_flex_335_v2_0 import range_bearing_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic.bsi_flex_335_v2_0.location import LocationList

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    RangeBearingCoordinateSystem: TypeAlias = (
        range_bearing_pb2.RangeBearingCoordinateSystem
    )
    RangeBearingDatum: TypeAlias = range_bearing_pb2.RangeBearingDatum
else:
    RangeBearingCoordinateSystem = int
    RangeBearingDatum = int


class RangeBearing(SapientModel):
    pb2_cls: ClassVar = range_bearing_pb2.RangeBearing

    # All fields are `optional` in the .proto; mandatory ones are enforced
    # only at to_pb2() by `_require_mandatory()`.
    elevation: float | None = None
    azimuth: float | None = None
    range: float | None = None
    elevation_error: float | None = None
    azimuth_error: float | None = None
    range_error: float | None = None
    coordinate_system: RangeBearingCoordinateSystem | None = None
    datum: RangeBearingDatum | None = None

    def to_pb2(self) -> range_bearing_pb2.RangeBearing:
        self._require_mandatory()
        msg = range_bearing_pb2.RangeBearing()
        if self.elevation is not None:
            msg.elevation = self.elevation
        if self.azimuth is not None:
            msg.azimuth = self.azimuth
        if self.range is not None:
            msg.range = self.range
        if self.elevation_error is not None:
            msg.elevation_error = self.elevation_error
        if self.azimuth_error is not None:
            msg.azimuth_error = self.azimuth_error
        if self.range_error is not None:
            msg.range_error = self.range_error
        if self.coordinate_system is not None:
            msg.coordinate_system = self.coordinate_system
        if self.datum is not None:
            msg.datum = self.datum
        return msg

    @classmethod
    def from_pb2(cls, msg: range_bearing_pb2.RangeBearing) -> Self:
        model = cls(
            elevation=msg.elevation if msg.HasField("elevation") else None,
            azimuth=msg.azimuth if msg.HasField("azimuth") else None,
            range=msg.range if msg.HasField("range") else None,
            elevation_error=(
                msg.elevation_error if msg.HasField("elevation_error") else None
            ),
            azimuth_error=msg.azimuth_error if msg.HasField("azimuth_error") else None,
            range_error=msg.range_error if msg.HasField("range_error") else None,
            coordinate_system=(
                msg.coordinate_system if msg.HasField("coordinate_system") else None
            ),
            datum=msg.datum if msg.HasField("datum") else None,
        )
        model._require_mandatory()
        return model


class RangeBearingCone(SapientModel):
    pb2_cls: ClassVar = range_bearing_pb2.RangeBearingCone

    elevation: float | None = None
    azimuth: float | None = None
    range: float | None = None
    horizontal_extent: float | None = None
    vertical_extent: float | None = None
    horizontal_extent_error: float | None = None
    vertical_extent_error: float | None = None
    elevation_error: float | None = None
    azimuth_error: float | None = None
    range_error: float | None = None
    coordinate_system: RangeBearingCoordinateSystem | None = None
    datum: RangeBearingDatum | None = None

    def to_pb2(self) -> range_bearing_pb2.RangeBearingCone:
        self._require_mandatory()
        msg = range_bearing_pb2.RangeBearingCone()
        if self.elevation is not None:
            msg.elevation = self.elevation
        if self.azimuth is not None:
            msg.azimuth = self.azimuth
        if self.range is not None:
            msg.range = self.range
        if self.horizontal_extent is not None:
            msg.horizontal_extent = self.horizontal_extent
        if self.vertical_extent is not None:
            msg.vertical_extent = self.vertical_extent
        if self.horizontal_extent_error is not None:
            msg.horizontal_extent_error = self.horizontal_extent_error
        if self.vertical_extent_error is not None:
            msg.vertical_extent_error = self.vertical_extent_error
        if self.elevation_error is not None:
            msg.elevation_error = self.elevation_error
        if self.azimuth_error is not None:
            msg.azimuth_error = self.azimuth_error
        if self.range_error is not None:
            msg.range_error = self.range_error
        if self.coordinate_system is not None:
            msg.coordinate_system = self.coordinate_system
        if self.datum is not None:
            msg.datum = self.datum
        return msg

    @classmethod
    def from_pb2(cls, msg: range_bearing_pb2.RangeBearingCone) -> Self:
        model = cls(
            elevation=msg.elevation if msg.HasField("elevation") else None,
            azimuth=msg.azimuth if msg.HasField("azimuth") else None,
            range=msg.range if msg.HasField("range") else None,
            horizontal_extent=(
                msg.horizontal_extent if msg.HasField("horizontal_extent") else None
            ),
            vertical_extent=(
                msg.vertical_extent if msg.HasField("vertical_extent") else None
            ),
            horizontal_extent_error=(
                msg.horizontal_extent_error
                if msg.HasField("horizontal_extent_error")
                else None
            ),
            vertical_extent_error=(
                msg.vertical_extent_error
                if msg.HasField("vertical_extent_error")
                else None
            ),
            elevation_error=(
                msg.elevation_error if msg.HasField("elevation_error") else None
            ),
            azimuth_error=msg.azimuth_error if msg.HasField("azimuth_error") else None,
            range_error=msg.range_error if msg.HasField("range_error") else None,
            coordinate_system=(
                msg.coordinate_system if msg.HasField("coordinate_system") else None
            ),
            datum=msg.datum if msg.HasField("datum") else None,
        )
        model._require_mandatory()
        return model


class LocationOrRangeBearing(SapientModel):
    pb2_cls: ClassVar = range_bearing_pb2.LocationOrRangeBearing

    # `fov_oneof` is a mandatory oneof: exactly one of these two must be set.
    range_bearing: RangeBearingCone | None = None
    location_list: LocationList | None = None

    def to_pb2(self) -> range_bearing_pb2.LocationOrRangeBearing:
        self._require_mandatory()
        msg = range_bearing_pb2.LocationOrRangeBearing()
        if self.range_bearing is not None:
            msg.range_bearing.CopyFrom(self.range_bearing.to_pb2())
        if self.location_list is not None:
            msg.location_list.CopyFrom(self.location_list.to_pb2())
        return msg

    @classmethod
    def from_pb2(cls, msg: range_bearing_pb2.LocationOrRangeBearing) -> Self:
        model = cls(
            range_bearing=(
                RangeBearingCone.from_pb2(msg.range_bearing)
                if msg.HasField("range_bearing")
                else None
            ),
            location_list=(
                LocationList.from_pb2(msg.location_list)
                if msg.HasField("location_list")
                else None
            ),
        )
        model._require_mandatory()
        return model
