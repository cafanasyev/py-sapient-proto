"""Pydantic models for registration.proto (largest module: ~27 nested messages).

Every nested message declared inside `Registration` in the .proto becomes a
FLAT top-level model here (e.g. `Registration.NodeDefinition` -> `NodeDefinition`),
named exactly as `external/sapient/builder/registration.py` does. That file is a
one-directional (`to_sapient()`-only) reference for field shapes; the descriptor
walker governs the actual field list (it surfaces several messages/fields the
reference port omits: `reporting_region`, `GeometricError`, `PerformanceValue`,
`BehaviourDefinition`, `Command`, `ClassFilterDefinition`,
`SubClassFilterDefinition`, `FilterParameter`, `BehaviourFilterDefinition`,
`TaxonomyDockDefinition`, `ExtensionSubclass`) -- all of those are implemented
here too, in both directions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeAlias

from pydantic import Field
from sapient_msg.bsi_flex_335_v2_0 import (
    location_pb2,
    range_bearing_pb2,
    registration_pb2,
)
from typing_extensions import Self

from sapient_msg_pydantic._base import SapientModel
from sapient_msg_pydantic.bsi_flex_335_v2_0.range_bearing import (
    LocationOrRangeBearing,
)
from sapient_msg_pydantic.bsi_flex_335_v2_0.velocity import ENUVelocityUnits

ICD_VERSION = "BSI Flex 335 v2.0"

if TYPE_CHECKING:
    # Real pb2 enum types for mypy; plain int at runtime for pydantic.
    Operator: TypeAlias = registration_pb2.Operator
    NodeType: TypeAlias = registration_pb2.Registration.NodeType
    TimeUnits: TypeAlias = registration_pb2.Registration.TimeUnits
    StatusReportCategory: TypeAlias = (
        registration_pb2.Registration.StatusReportCategory
    )
    ModeType: TypeAlias = registration_pb2.Registration.ModeType
    ScanType: TypeAlias = registration_pb2.Registration.ScanType
    TrackingType: TypeAlias = registration_pb2.Registration.TrackingType
    DetectionReportCategory: TypeAlias = (
        registration_pb2.Registration.DetectionReportCategory
    )
    ConfidenceDefinition: TypeAlias = (
        registration_pb2.Registration.ConfidenceDefinition
    )
    CommandType: TypeAlias = registration_pb2.Registration.CommandType
    RegionType: TypeAlias = registration_pb2.Registration.RegionType
    LocationCoordinateSystem: TypeAlias = (
        location_pb2.LocationCoordinateSystem
    )
    LocationDatum: TypeAlias = location_pb2.LocationDatum
    RangeBearingCoordinateSystem: TypeAlias = (
        range_bearing_pb2.RangeBearingCoordinateSystem
    )
    RangeBearingDatum: TypeAlias = range_bearing_pb2.RangeBearingDatum
else:
    Operator = int
    NodeType = int
    TimeUnits = int
    StatusReportCategory = int
    ModeType = int
    ScanType = int
    TrackingType = int
    DetectionReportCategory = int
    ConfidenceDefinition = int
    CommandType = int
    RegionType = int
    LocationCoordinateSystem = int
    LocationDatum = int
    RangeBearingCoordinateSystem = int
    RangeBearingDatum = int


class NodeDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.NodeDefinition

    node_type: NodeType | None = None
    node_sub_type: list[str] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.NodeDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.NodeDefinition()
        if self.node_type is not None:
            msg.node_type = self.node_type
        msg.node_sub_type.extend(self.node_sub_type)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.NodeDefinition) -> Self:
        model = cls(
            node_type=msg.node_type if msg.HasField("node_type") else None,
            node_sub_type=list(msg.node_sub_type),
        )
        model._require_mandatory()
        return model


class Capability(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.Capability

    category: str | None = None
    type: str | None = None
    value: str | None = None
    units: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.Capability:
        self._require_mandatory()
        msg = registration_pb2.Registration.Capability()
        if self.category is not None:
            msg.category = self.category
        if self.type is not None:
            msg.type = self.type
        if self.value is not None:
            msg.value = self.value
        if self.units is not None:
            msg.units = self.units
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.Capability) -> Self:
        model = cls(
            category=msg.category if msg.HasField("category") else None,
            type=msg.type if msg.HasField("type") else None,
            value=msg.value if msg.HasField("value") else None,
            units=msg.units if msg.HasField("units") else None,
        )
        model._require_mandatory()
        return model


class Duration(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.Duration

    units: TimeUnits | None = None
    value: float | None = None

    def to_pb2(self) -> registration_pb2.Registration.Duration:
        self._require_mandatory()
        msg = registration_pb2.Registration.Duration()
        if self.units is not None:
            msg.units = self.units
        if self.value is not None:
            msg.value = self.value
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.Duration) -> Self:
        model = cls(
            units=msg.units if msg.HasField("units") else None,
            value=msg.value if msg.HasField("value") else None,
        )
        model._require_mandatory()
        return model


class ModeParameter(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.ModeParameter

    type: str | None = None
    value: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.ModeParameter:
        self._require_mandatory()
        msg = registration_pb2.Registration.ModeParameter()
        if self.type is not None:
            msg.type = self.type
        if self.value is not None:
            msg.value = self.value
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.ModeParameter) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            value=msg.value if msg.HasField("value") else None,
        )
        model._require_mandatory()
        return model


class LocationType(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.LocationType

    # `coordinates_oneof` (location_units | range_bearing_units) and
    # `datum_oneof` (location_datum | range_bearing_datum) are both mandatory
    # oneofs: `_require_mandatory()` enforces exactly one member of each set.
    location_units: LocationCoordinateSystem | None = None
    range_bearing_units: RangeBearingCoordinateSystem | None = None
    location_datum: LocationDatum | None = None
    range_bearing_datum: RangeBearingDatum | None = None
    zone: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.LocationType:
        self._require_mandatory()
        msg = registration_pb2.Registration.LocationType()
        if self.location_units is not None:
            msg.location_units = self.location_units
        if self.range_bearing_units is not None:
            msg.range_bearing_units = self.range_bearing_units
        if self.location_datum is not None:
            msg.location_datum = self.location_datum
        if self.range_bearing_datum is not None:
            msg.range_bearing_datum = self.range_bearing_datum
        if self.zone is not None:
            msg.zone = self.zone
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.LocationType) -> Self:
        model = cls(
            location_units=(
                msg.location_units if msg.HasField("location_units") else None
            ),
            range_bearing_units=(
                msg.range_bearing_units
                if msg.HasField("range_bearing_units")
                else None
            ),
            location_datum=(
                msg.location_datum if msg.HasField("location_datum") else None
            ),
            range_bearing_datum=(
                msg.range_bearing_datum
                if msg.HasField("range_bearing_datum")
                else None
            ),
            zone=msg.zone if msg.HasField("zone") else None,
        )
        model._require_mandatory()
        return model


class VelocityType(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.VelocityType

    # `velocity_units_oneof` (only `enu_velocity_units` is live; the other
    # historical members are `reserved` in the .proto) and `datum_oneof`
    # (location_datum | range_bearing_datum) are both mandatory oneofs.
    enu_velocity_units: ENUVelocityUnits | None = None
    location_datum: LocationDatum | None = None
    range_bearing_datum: RangeBearingDatum | None = None
    zone: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.VelocityType:
        self._require_mandatory()
        msg = registration_pb2.Registration.VelocityType()
        if self.enu_velocity_units is not None:
            msg.enu_velocity_units.CopyFrom(self.enu_velocity_units.to_pb2())
        if self.location_datum is not None:
            msg.location_datum = self.location_datum
        if self.range_bearing_datum is not None:
            msg.range_bearing_datum = self.range_bearing_datum
        if self.zone is not None:
            msg.zone = self.zone
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.VelocityType) -> Self:
        model = cls(
            enu_velocity_units=(
                ENUVelocityUnits.from_pb2(msg.enu_velocity_units)
                if msg.HasField("enu_velocity_units")
                else None
            ),
            location_datum=(
                msg.location_datum if msg.HasField("location_datum") else None
            ),
            range_bearing_datum=(
                msg.range_bearing_datum
                if msg.HasField("range_bearing_datum")
                else None
            ),
            zone=msg.zone if msg.HasField("zone") else None,
        )
        model._require_mandatory()
        return model


class StatusReport(SapientModel):
    """Registration's own `StatusReport` (heartbeat field definition)."""

    pb2_cls: ClassVar = registration_pb2.Registration.StatusReport

    category: StatusReportCategory | None = None
    type: str | None = None
    units: str | None = None
    on_change: bool | None = None

    def to_pb2(self) -> registration_pb2.Registration.StatusReport:
        self._require_mandatory()
        msg = registration_pb2.Registration.StatusReport()
        if self.category is not None:
            msg.category = self.category
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        if self.on_change is not None:
            msg.on_change = self.on_change
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.StatusReport) -> Self:
        model = cls(
            category=msg.category if msg.HasField("category") else None,
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            on_change=msg.on_change if msg.HasField("on_change") else None,
        )
        model._require_mandatory()
        return model


class PerformanceValue(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.PerformanceValue

    type: str | None = None
    units: str | None = None
    unit_value: str | None = None
    variation_type: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.PerformanceValue:
        self._require_mandatory()
        msg = registration_pb2.Registration.PerformanceValue()
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        if self.unit_value is not None:
            msg.unit_value = self.unit_value
        if self.variation_type is not None:
            msg.variation_type = self.variation_type
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.PerformanceValue) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            unit_value=msg.unit_value if msg.HasField("unit_value") else None,
            variation_type=(
                msg.variation_type if msg.HasField("variation_type") else None
            ),
        )
        model._require_mandatory()
        return model


class GeometricError(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.GeometricError

    type: str | None = None
    units: str | None = None
    variation_type: str | None = None
    performance_value: list[PerformanceValue] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.GeometricError:
        self._require_mandatory()
        msg = registration_pb2.Registration.GeometricError()
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        if self.variation_type is not None:
            msg.variation_type = self.variation_type
        msg.performance_value.extend(x.to_pb2() for x in self.performance_value)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.GeometricError) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            variation_type=(
                msg.variation_type if msg.HasField("variation_type") else None
            ),
            performance_value=[
                PerformanceValue.from_pb2(x) for x in msg.performance_value
            ],
        )
        model._require_mandatory()
        return model


class DetectionReport(SapientModel):
    """Registration's own `DetectionReport` (detection field definition)."""

    pb2_cls: ClassVar = registration_pb2.Registration.DetectionReport

    category: DetectionReportCategory | None = None
    type: str | None = None
    units: str | None = None
    on_change: bool | None = None

    def to_pb2(self) -> registration_pb2.Registration.DetectionReport:
        self._require_mandatory()
        msg = registration_pb2.Registration.DetectionReport()
        if self.category is not None:
            msg.category = self.category
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        if self.on_change is not None:
            msg.on_change = self.on_change
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.DetectionReport) -> Self:
        model = cls(
            category=msg.category if msg.HasField("category") else None,
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            on_change=msg.on_change if msg.HasField("on_change") else None,
        )
        model._require_mandatory()
        return model


class BehaviourDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.BehaviourDefinition

    type: str | None = None
    units: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.BehaviourDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.BehaviourDefinition()
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.BehaviourDefinition
    ) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
        )
        model._require_mandatory()
        return model


class SubClass(SapientModel):
    """Self-referential taxonomy node: `sub_class: List[SubClass]`.

    Direct self-reference within the same class body resolves fine under
    pydantic v2 without an explicit `model_rebuild()` call (the class name is
    already bound in module globals by the time any instance is built/
    validated); `model_rebuild()` is only added if that assumption breaks.
    """

    pb2_cls: ClassVar = registration_pb2.Registration.SubClass

    type: str | None = None
    units: str | None = None
    level: int | None = None
    sub_class: list[SubClass] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.SubClass:
        self._require_mandatory()
        msg = registration_pb2.Registration.SubClass()
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        if self.level is not None:
            msg.level = self.level
        msg.sub_class.extend(x.to_pb2() for x in self.sub_class)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.SubClass) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            level=msg.level if msg.HasField("level") else None,
            sub_class=[SubClass.from_pb2(x) for x in msg.sub_class],
        )
        model._require_mandatory()
        return model


class ClassDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.ClassDefinition

    type: str | None = None
    units: str | None = None
    sub_class: list[SubClass] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.ClassDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.ClassDefinition()
        if self.type is not None:
            msg.type = self.type
        if self.units is not None:
            msg.units = self.units
        msg.sub_class.extend(x.to_pb2() for x in self.sub_class)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.ClassDefinition) -> Self:
        model = cls(
            type=msg.type if msg.HasField("type") else None,
            units=msg.units if msg.HasField("units") else None,
            sub_class=[SubClass.from_pb2(x) for x in msg.sub_class],
        )
        model._require_mandatory()
        return model


class ExtensionSubclass(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.ExtensionSubclass

    # Field names below are declared with this exact (non-lowercase) casing
    # in the .proto (`Subclass_namespace`, `Subclass_name`) -- protoc keeps
    # proto field names verbatim as the generated Python attribute names, so
    # the model fields must match exactly for msg.<field>/HasField to work.
    Subclass_namespace: str | None = None
    Subclass_name: str | None = None
    units: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.ExtensionSubclass:
        self._require_mandatory()
        msg = registration_pb2.Registration.ExtensionSubclass()
        if self.Subclass_namespace is not None:
            msg.Subclass_namespace = self.Subclass_namespace
        if self.Subclass_name is not None:
            msg.Subclass_name = self.Subclass_name
        if self.units is not None:
            msg.units = self.units
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.ExtensionSubclass
    ) -> Self:
        model = cls(
            Subclass_namespace=(
                msg.Subclass_namespace
                if msg.HasField("Subclass_namespace")
                else None
            ),
            Subclass_name=(
                msg.Subclass_name if msg.HasField("Subclass_name") else None
            ),
            units=msg.units if msg.HasField("units") else None,
        )
        model._require_mandatory()
        return model


class TaxonomyDockDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.TaxonomyDockDefinition

    # Same non-lowercase-verbatim-field-name note as ExtensionSubclass above.
    Dock_class_namespace: str | None = None
    Dock_class: str | None = None
    Extension_subclass: list[ExtensionSubclass] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.TaxonomyDockDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.TaxonomyDockDefinition()
        if self.Dock_class_namespace is not None:
            msg.Dock_class_namespace = self.Dock_class_namespace
        if self.Dock_class is not None:
            msg.Dock_class = self.Dock_class
        msg.Extension_subclass.extend(
            x.to_pb2() for x in self.Extension_subclass
        )
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.TaxonomyDockDefinition
    ) -> Self:
        model = cls(
            Dock_class_namespace=(
                msg.Dock_class_namespace
                if msg.HasField("Dock_class_namespace")
                else None
            ),
            Dock_class=(
                msg.Dock_class if msg.HasField("Dock_class") else None
            ),
            Extension_subclass=[
                ExtensionSubclass.from_pb2(x) for x in msg.Extension_subclass
            ],
        )
        model._require_mandatory()
        return model


class DetectionClassDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.DetectionClassDefinition

    confidence_definition: ConfidenceDefinition | None = None
    class_performance: list[PerformanceValue] = Field(default_factory=list)
    class_definition: list[ClassDefinition] = Field(default_factory=list)
    taxonomy_dock_definition: list[TaxonomyDockDefinition] = Field(
        default_factory=list
    )

    def to_pb2(self) -> registration_pb2.Registration.DetectionClassDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.DetectionClassDefinition()
        if self.confidence_definition is not None:
            msg.confidence_definition = self.confidence_definition
        msg.class_performance.extend(x.to_pb2() for x in self.class_performance)
        msg.class_definition.extend(x.to_pb2() for x in self.class_definition)
        msg.taxonomy_dock_definition.extend(
            x.to_pb2() for x in self.taxonomy_dock_definition
        )
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.DetectionClassDefinition
    ) -> Self:
        model = cls(
            confidence_definition=(
                msg.confidence_definition
                if msg.HasField("confidence_definition")
                else None
            ),
            class_performance=[
                PerformanceValue.from_pb2(x) for x in msg.class_performance
            ],
            class_definition=[
                ClassDefinition.from_pb2(x) for x in msg.class_definition
            ],
            taxonomy_dock_definition=[
                TaxonomyDockDefinition.from_pb2(x)
                for x in msg.taxonomy_dock_definition
            ],
        )
        model._require_mandatory()
        return model


class DetectionDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.DetectionDefinition

    location_type: LocationType | None = None
    detection_performance: list[PerformanceValue] = Field(default_factory=list)
    detection_report: list[DetectionReport] = Field(default_factory=list)
    detection_class_definition: list[DetectionClassDefinition] = Field(
        default_factory=list
    )
    behaviour_definition: list[BehaviourDefinition] = Field(default_factory=list)
    velocity_type: VelocityType | None = None
    geometric_error: GeometricError | None = None

    def to_pb2(self) -> registration_pb2.Registration.DetectionDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.DetectionDefinition()
        if self.location_type is not None:
            msg.location_type.CopyFrom(self.location_type.to_pb2())
        msg.detection_performance.extend(
            x.to_pb2() for x in self.detection_performance
        )
        msg.detection_report.extend(x.to_pb2() for x in self.detection_report)
        msg.detection_class_definition.extend(
            x.to_pb2() for x in self.detection_class_definition
        )
        msg.behaviour_definition.extend(
            x.to_pb2() for x in self.behaviour_definition
        )
        if self.velocity_type is not None:
            msg.velocity_type.CopyFrom(self.velocity_type.to_pb2())
        if self.geometric_error is not None:
            msg.geometric_error.CopyFrom(self.geometric_error.to_pb2())
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.DetectionDefinition
    ) -> Self:
        model = cls(
            location_type=(
                LocationType.from_pb2(msg.location_type)
                if msg.HasField("location_type")
                else None
            ),
            detection_performance=[
                PerformanceValue.from_pb2(x) for x in msg.detection_performance
            ],
            detection_report=[
                DetectionReport.from_pb2(x) for x in msg.detection_report
            ],
            detection_class_definition=[
                DetectionClassDefinition.from_pb2(x)
                for x in msg.detection_class_definition
            ],
            behaviour_definition=[
                BehaviourDefinition.from_pb2(x) for x in msg.behaviour_definition
            ],
            velocity_type=(
                VelocityType.from_pb2(msg.velocity_type)
                if msg.HasField("velocity_type")
                else None
            ),
            geometric_error=(
                GeometricError.from_pb2(msg.geometric_error)
                if msg.HasField("geometric_error")
                else None
            ),
        )
        model._require_mandatory()
        return model


class FilterParameter(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.FilterParameter

    parameter: str | None = None
    operators: list[Operator] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.FilterParameter:
        self._require_mandatory()
        msg = registration_pb2.Registration.FilterParameter()
        if self.parameter is not None:
            msg.parameter = self.parameter
        msg.operators.extend(self.operators)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.FilterParameter) -> Self:
        model = cls(
            parameter=msg.parameter if msg.HasField("parameter") else None,
            operators=list(msg.operators),
        )
        model._require_mandatory()
        return model


class SubClassFilterDefinition(SapientModel):
    """Self-referential filter node: `sub_class_definition: List[Self]`."""

    pb2_cls: ClassVar = registration_pb2.Registration.SubClassFilterDefinition

    filter_parameter: list[FilterParameter] = Field(default_factory=list)
    level: int | None = None
    type: str | None = None
    sub_class_definition: list[SubClassFilterDefinition] = Field(
        default_factory=list
    )

    def to_pb2(self) -> registration_pb2.Registration.SubClassFilterDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.SubClassFilterDefinition()
        msg.filter_parameter.extend(x.to_pb2() for x in self.filter_parameter)
        if self.level is not None:
            msg.level = self.level
        if self.type is not None:
            msg.type = self.type
        msg.sub_class_definition.extend(
            x.to_pb2() for x in self.sub_class_definition
        )
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.SubClassFilterDefinition
    ) -> Self:
        model = cls(
            filter_parameter=[
                FilterParameter.from_pb2(x) for x in msg.filter_parameter
            ],
            level=msg.level if msg.HasField("level") else None,
            type=msg.type if msg.HasField("type") else None,
            sub_class_definition=[
                SubClassFilterDefinition.from_pb2(x)
                for x in msg.sub_class_definition
            ],
        )
        model._require_mandatory()
        return model


class ClassFilterDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.ClassFilterDefinition

    filter_parameter: list[FilterParameter] = Field(default_factory=list)
    sub_class_definition: list[SubClassFilterDefinition] = Field(
        default_factory=list
    )
    type: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.ClassFilterDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.ClassFilterDefinition()
        msg.filter_parameter.extend(x.to_pb2() for x in self.filter_parameter)
        msg.sub_class_definition.extend(
            x.to_pb2() for x in self.sub_class_definition
        )
        if self.type is not None:
            msg.type = self.type
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.ClassFilterDefinition
    ) -> Self:
        model = cls(
            filter_parameter=[
                FilterParameter.from_pb2(x) for x in msg.filter_parameter
            ],
            sub_class_definition=[
                SubClassFilterDefinition.from_pb2(x)
                for x in msg.sub_class_definition
            ],
            type=msg.type if msg.HasField("type") else None,
        )
        model._require_mandatory()
        return model


class BehaviourFilterDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.BehaviourFilterDefinition

    filter_parameter: list[FilterParameter] = Field(default_factory=list)
    type: str | None = None

    def to_pb2(self) -> registration_pb2.Registration.BehaviourFilterDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.BehaviourFilterDefinition()
        msg.filter_parameter.extend(x.to_pb2() for x in self.filter_parameter)
        if self.type is not None:
            msg.type = self.type
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.BehaviourFilterDefinition
    ) -> Self:
        model = cls(
            filter_parameter=[
                FilterParameter.from_pb2(x) for x in msg.filter_parameter
            ],
            type=msg.type if msg.HasField("type") else None,
        )
        model._require_mandatory()
        return model


class Command(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.Command

    units: str | None = None
    completion_time: Duration | None = None
    type: CommandType | None = None

    def to_pb2(self) -> registration_pb2.Registration.Command:
        self._require_mandatory()
        msg = registration_pb2.Registration.Command()
        if self.units is not None:
            msg.units = self.units
        if self.completion_time is not None:
            msg.completion_time.CopyFrom(self.completion_time.to_pb2())
        if self.type is not None:
            msg.type = self.type
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.Command) -> Self:
        model = cls(
            units=msg.units if msg.HasField("units") else None,
            completion_time=(
                Duration.from_pb2(msg.completion_time)
                if msg.HasField("completion_time")
                else None
            ),
            type=msg.type if msg.HasField("type") else None,
        )
        model._require_mandatory()
        return model


class RegionDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.RegionDefinition

    region_type: list[RegionType] = Field(default_factory=list)
    settle_time: Duration | None = None
    region_area: list[LocationType] = Field(default_factory=list)
    class_filter_definition: list[ClassFilterDefinition] = Field(
        default_factory=list
    )
    behaviour_filter_definition: list[BehaviourFilterDefinition] = Field(
        default_factory=list
    )

    def to_pb2(self) -> registration_pb2.Registration.RegionDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.RegionDefinition()
        msg.region_type.extend(self.region_type)
        if self.settle_time is not None:
            msg.settle_time.CopyFrom(self.settle_time.to_pb2())
        msg.region_area.extend(x.to_pb2() for x in self.region_area)
        msg.class_filter_definition.extend(
            x.to_pb2() for x in self.class_filter_definition
        )
        msg.behaviour_filter_definition.extend(
            x.to_pb2() for x in self.behaviour_filter_definition
        )
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.RegionDefinition) -> Self:
        model = cls(
            region_type=list(msg.region_type),
            settle_time=(
                Duration.from_pb2(msg.settle_time)
                if msg.HasField("settle_time")
                else None
            ),
            region_area=[LocationType.from_pb2(x) for x in msg.region_area],
            class_filter_definition=[
                ClassFilterDefinition.from_pb2(x)
                for x in msg.class_filter_definition
            ],
            behaviour_filter_definition=[
                BehaviourFilterDefinition.from_pb2(x)
                for x in msg.behaviour_filter_definition
            ],
        )
        model._require_mandatory()
        return model


class TaskDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.TaskDefinition

    concurrent_tasks: int | None = None
    region_definition: RegionDefinition | None = None
    command: list[Command] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.TaskDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.TaskDefinition()
        if self.concurrent_tasks is not None:
            msg.concurrent_tasks = self.concurrent_tasks
        if self.region_definition is not None:
            msg.region_definition.CopyFrom(self.region_definition.to_pb2())
        msg.command.extend(x.to_pb2() for x in self.command)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.TaskDefinition) -> Self:
        model = cls(
            concurrent_tasks=(
                msg.concurrent_tasks if msg.HasField("concurrent_tasks") else None
            ),
            region_definition=(
                RegionDefinition.from_pb2(msg.region_definition)
                if msg.HasField("region_definition")
                else None
            ),
            command=[Command.from_pb2(x) for x in msg.command],
        )
        model._require_mandatory()
        return model


class ModeDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.ModeDefinition

    mode_name: str | None = None
    mode_type: ModeType | None = None
    mode_description: str | None = None
    settle_time: Duration | None = None
    maximum_latency: Duration | None = None
    scan_type: ScanType | None = None
    tracking_type: TrackingType | None = None
    duration: Duration | None = None
    mode_parameter: list[ModeParameter] = Field(default_factory=list)
    detection_definition: list[DetectionDefinition] = Field(default_factory=list)
    task: TaskDefinition | None = None

    def to_pb2(self) -> registration_pb2.Registration.ModeDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.ModeDefinition()
        if self.mode_name is not None:
            msg.mode_name = self.mode_name
        if self.mode_type is not None:
            msg.mode_type = self.mode_type
        if self.mode_description is not None:
            msg.mode_description = self.mode_description
        if self.settle_time is not None:
            msg.settle_time.CopyFrom(self.settle_time.to_pb2())
        if self.maximum_latency is not None:
            msg.maximum_latency.CopyFrom(self.maximum_latency.to_pb2())
        if self.scan_type is not None:
            msg.scan_type = self.scan_type
        if self.tracking_type is not None:
            msg.tracking_type = self.tracking_type
        if self.duration is not None:
            msg.duration.CopyFrom(self.duration.to_pb2())
        msg.mode_parameter.extend(x.to_pb2() for x in self.mode_parameter)
        msg.detection_definition.extend(
            x.to_pb2() for x in self.detection_definition
        )
        if self.task is not None:
            msg.task.CopyFrom(self.task.to_pb2())
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.ModeDefinition) -> Self:
        model = cls(
            mode_name=msg.mode_name if msg.HasField("mode_name") else None,
            mode_type=msg.mode_type if msg.HasField("mode_type") else None,
            mode_description=(
                msg.mode_description if msg.HasField("mode_description") else None
            ),
            settle_time=(
                Duration.from_pb2(msg.settle_time)
                if msg.HasField("settle_time")
                else None
            ),
            maximum_latency=(
                Duration.from_pb2(msg.maximum_latency)
                if msg.HasField("maximum_latency")
                else None
            ),
            scan_type=msg.scan_type if msg.HasField("scan_type") else None,
            tracking_type=(
                msg.tracking_type if msg.HasField("tracking_type") else None
            ),
            duration=(
                Duration.from_pb2(msg.duration)
                if msg.HasField("duration")
                else None
            ),
            mode_parameter=[
                ModeParameter.from_pb2(x) for x in msg.mode_parameter
            ],
            detection_definition=[
                DetectionDefinition.from_pb2(x) for x in msg.detection_definition
            ],
            task=(
                TaskDefinition.from_pb2(msg.task) if msg.HasField("task") else None
            ),
        )
        model._require_mandatory()
        return model


class StatusDefinition(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration.StatusDefinition

    status_interval: Duration | None = None
    location_definition: LocationType | None = None
    coverage_definition: LocationType | None = None
    obscuration_definition: LocationType | None = None
    status_report: list[StatusReport] = Field(default_factory=list)
    field_of_view_definition: LocationType | None = None

    def to_pb2(self) -> registration_pb2.Registration.StatusDefinition:
        self._require_mandatory()
        msg = registration_pb2.Registration.StatusDefinition()
        if self.status_interval is not None:
            msg.status_interval.CopyFrom(self.status_interval.to_pb2())
        if self.location_definition is not None:
            msg.location_definition.CopyFrom(self.location_definition.to_pb2())
        if self.coverage_definition is not None:
            msg.coverage_definition.CopyFrom(self.coverage_definition.to_pb2())
        if self.obscuration_definition is not None:
            msg.obscuration_definition.CopyFrom(
                self.obscuration_definition.to_pb2()
            )
        msg.status_report.extend(x.to_pb2() for x in self.status_report)
        if self.field_of_view_definition is not None:
            msg.field_of_view_definition.CopyFrom(
                self.field_of_view_definition.to_pb2()
            )
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration.StatusDefinition) -> Self:
        model = cls(
            status_interval=(
                Duration.from_pb2(msg.status_interval)
                if msg.HasField("status_interval")
                else None
            ),
            location_definition=(
                LocationType.from_pb2(msg.location_definition)
                if msg.HasField("location_definition")
                else None
            ),
            coverage_definition=(
                LocationType.from_pb2(msg.coverage_definition)
                if msg.HasField("coverage_definition")
                else None
            ),
            obscuration_definition=(
                LocationType.from_pb2(msg.obscuration_definition)
                if msg.HasField("obscuration_definition")
                else None
            ),
            status_report=[StatusReport.from_pb2(x) for x in msg.status_report],
            field_of_view_definition=(
                LocationType.from_pb2(msg.field_of_view_definition)
                if msg.HasField("field_of_view_definition")
                else None
            ),
        )
        model._require_mandatory()
        return model


class ConfigurationData(SapientModel):
    """Self-referential: `sub_components: List[ConfigurationData]`.

    NOTE: `manufacturer`/`model` are declared WITHOUT `optional` in the
    .proto (plain `string manufacturer = 1 [...is_mandatory: true]`), so the
    descriptor walker reports has_presence=False for both even though they
    are mandatory -- the same presence-less-mandatory shape as
    `follow.FollowObject.follow_object_id` (Task 4). They get the
    non-optional, proto-default treatment (direct assignment, no HasField);
    `_require_mandatory()` still rejects the empty-string default.
    """

    pb2_cls: ClassVar = registration_pb2.Registration.ConfigurationData

    manufacturer: str = ""
    model: str = ""
    serial_number: str | None = None
    hardware_version: str | None = None
    software_version: str | None = None
    sub_components: list[ConfigurationData] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration.ConfigurationData:
        self._require_mandatory()
        msg = registration_pb2.Registration.ConfigurationData()
        msg.manufacturer = self.manufacturer
        msg.model = self.model
        if self.serial_number is not None:
            msg.serial_number = self.serial_number
        if self.hardware_version is not None:
            msg.hardware_version = self.hardware_version
        if self.software_version is not None:
            msg.software_version = self.software_version
        msg.sub_components.extend(x.to_pb2() for x in self.sub_components)
        return msg

    @classmethod
    def from_pb2(
        cls, msg: registration_pb2.Registration.ConfigurationData
    ) -> Self:
        model = cls(
            manufacturer=msg.manufacturer,
            model=msg.model,
            serial_number=(
                msg.serial_number if msg.HasField("serial_number") else None
            ),
            hardware_version=(
                msg.hardware_version if msg.HasField("hardware_version") else None
            ),
            software_version=(
                msg.software_version if msg.HasField("software_version") else None
            ),
            sub_components=[
                ConfigurationData.from_pb2(x) for x in msg.sub_components
            ],
        )
        model._require_mandatory()
        return model


class Registration(SapientModel):
    pb2_cls: ClassVar = registration_pb2.Registration

    # node_definition/capabilities/mode_definition/config_data are `repeated`
    # yet `is_mandatory`: `_require_mandatory()` treats an empty list as unset.
    node_definition: list[NodeDefinition] = Field(default_factory=list)
    icd_version: str | None = ICD_VERSION
    name: str | None = None
    short_name: str | None = None
    capabilities: list[Capability] = Field(default_factory=list)
    status_definition: StatusDefinition | None = None
    mode_definition: list[ModeDefinition] = Field(default_factory=list)
    dependent_nodes: list[str] = Field(default_factory=list)
    reporting_region: list[LocationOrRangeBearing] = Field(default_factory=list)
    config_data: list[ConfigurationData] = Field(default_factory=list)

    def to_pb2(self) -> registration_pb2.Registration:
        self._require_mandatory()
        msg = registration_pb2.Registration()
        msg.node_definition.extend(x.to_pb2() for x in self.node_definition)
        if self.icd_version is not None:
            msg.icd_version = self.icd_version
        if self.name is not None:
            msg.name = self.name
        if self.short_name is not None:
            msg.short_name = self.short_name
        msg.capabilities.extend(x.to_pb2() for x in self.capabilities)
        if self.status_definition is not None:
            msg.status_definition.CopyFrom(self.status_definition.to_pb2())
        msg.mode_definition.extend(x.to_pb2() for x in self.mode_definition)
        msg.dependent_nodes.extend(self.dependent_nodes)
        msg.reporting_region.extend(x.to_pb2() for x in self.reporting_region)
        msg.config_data.extend(x.to_pb2() for x in self.config_data)
        return msg

    @classmethod
    def from_pb2(cls, msg: registration_pb2.Registration) -> Self:
        model = cls(
            node_definition=[
                NodeDefinition.from_pb2(x) for x in msg.node_definition
            ],
            icd_version=msg.icd_version if msg.HasField("icd_version") else None,
            name=msg.name if msg.HasField("name") else None,
            short_name=msg.short_name if msg.HasField("short_name") else None,
            capabilities=[Capability.from_pb2(x) for x in msg.capabilities],
            status_definition=(
                StatusDefinition.from_pb2(msg.status_definition)
                if msg.HasField("status_definition")
                else None
            ),
            mode_definition=[
                ModeDefinition.from_pb2(x) for x in msg.mode_definition
            ],
            dependent_nodes=list(msg.dependent_nodes),
            reporting_region=[
                LocationOrRangeBearing.from_pb2(x) for x in msg.reporting_region
            ],
            config_data=[ConfigurationData.from_pb2(x) for x in msg.config_data],
        )
        model._require_mandatory()
        return model
