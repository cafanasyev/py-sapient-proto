"""Pydantic models for velocity.proto."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from sapient_msg.bsi_flex_335_v2_0 import velocity_pb2
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    SpeedUnits: TypeAlias = velocity_pb2.SpeedUnits
else:
    SpeedUnits = int


class ENUVelocity(SapientModel):
    pb2_cls: ClassVar = velocity_pb2.ENUVelocity

    east_rate: float | None = None
    north_rate: float | None = None
    up_rate: float | None = None
    east_rate_error: float | None = None
    north_rate_error: float | None = None
    up_rate_error: float | None = None

    def to_pb2(self) -> velocity_pb2.ENUVelocity:
        self._require_mandatory()
        msg = velocity_pb2.ENUVelocity()
        if self.east_rate is not None:
            msg.east_rate = self.east_rate
        if self.north_rate is not None:
            msg.north_rate = self.north_rate
        if self.up_rate is not None:
            msg.up_rate = self.up_rate
        if self.east_rate_error is not None:
            msg.east_rate_error = self.east_rate_error
        if self.north_rate_error is not None:
            msg.north_rate_error = self.north_rate_error
        if self.up_rate_error is not None:
            msg.up_rate_error = self.up_rate_error
        return msg

    @classmethod
    def from_pb2(cls, msg: velocity_pb2.ENUVelocity) -> Self:
        model = cls(
            east_rate=msg.east_rate if msg.HasField("east_rate") else None,
            north_rate=msg.north_rate if msg.HasField("north_rate") else None,
            up_rate=msg.up_rate if msg.HasField("up_rate") else None,
            east_rate_error=(
                msg.east_rate_error if msg.HasField("east_rate_error") else None
            ),
            north_rate_error=(
                msg.north_rate_error if msg.HasField("north_rate_error") else None
            ),
            up_rate_error=msg.up_rate_error if msg.HasField("up_rate_error") else None,
        )
        model._require_mandatory()
        return model


class ENUVelocityUnits(SapientModel):
    pb2_cls: ClassVar = velocity_pb2.ENUVelocityUnits

    east_north_rate_units: SpeedUnits | None = None
    up_rate_units: SpeedUnits | None = None

    def to_pb2(self) -> velocity_pb2.ENUVelocityUnits:
        self._require_mandatory()
        msg = velocity_pb2.ENUVelocityUnits()
        if self.east_north_rate_units is not None:
            msg.east_north_rate_units = self.east_north_rate_units
        if self.up_rate_units is not None:
            msg.up_rate_units = self.up_rate_units
        return msg

    @classmethod
    def from_pb2(cls, msg: velocity_pb2.ENUVelocityUnits) -> Self:
        model = cls(
            east_north_rate_units=(
                msg.east_north_rate_units
                if msg.HasField("east_north_rate_units")
                else None
            ),
            up_rate_units=(
                msg.up_rate_units if msg.HasField("up_rate_units") else None
            ),
        )
        model._require_mandatory()
        return model
