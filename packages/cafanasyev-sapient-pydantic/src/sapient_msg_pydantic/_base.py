"""Shared pydantic base for all SAPIENT models."""
from __future__ import annotations

import uuid
from typing import Any, ClassVar

from google.protobuf.message import Message
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Self
from ulid import ULID

from sapient_msg_pydantic._options import (
    IcdValidationError,
    mandatory_fields,
    mandatory_oneofs,
    ulid_fields,
    uuid_fields,
)


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def _is_ulid(value: str) -> bool:
    try:
        ULID.from_str(value)
    except ValueError:
        return False
    return True


class SapientModel(BaseModel):
    """Base model: UUID/ULID format validation now, mandatory checks at to_pb2()."""

    model_config = ConfigDict(validate_assignment=True)

    pb2_cls: ClassVar[type[Message]]

    @model_validator(mode="after")
    def _check_id_formats(self) -> Self:
        descriptor = self.pb2_cls.DESCRIPTOR
        for name in uuid_fields(descriptor):
            value: Any = getattr(self, name, None)
            if value is not None and not _is_uuid(value):
                raise ValueError(f"{name}: {value!r} is not a valid UUID")
        for name in ulid_fields(descriptor):
            value = getattr(self, name, None)
            if value is not None and not _is_ulid(value):
                raise ValueError(f"{name}: {value!r} is not a valid ULID")
        return self

    def _require_mandatory(self) -> None:
        descriptor = self.pb2_cls.DESCRIPTOR
        missing = [
            name
            for name in sorted(mandatory_fields(descriptor))
            if hasattr(self, name)
            and (
                getattr(self, name) is None
                or getattr(self, name) == []
                or getattr(self, name) == ""
            )
        ]
        oneof_errors = []
        for oneof_name in sorted(mandatory_oneofs(descriptor)):
            members = [
                f.name for f in descriptor.oneofs_by_name[oneof_name].fields
            ]
            set_members = [
                m for m in members if getattr(self, m, None) is not None
            ]
            if len(set_members) != 1:
                oneof_errors.append(
                    f"oneof '{oneof_name}' must have exactly one of "
                    f"{members} set (got {len(set_members)})"
                )
        if missing or oneof_errors:
            parts = []
            if missing:
                parts.append(f"mandatory fields unset: {', '.join(missing)}")
            parts.extend(oneof_errors)
            raise IcdValidationError(
                f"{type(self).__name__}: " + "; ".join(parts)
            )
