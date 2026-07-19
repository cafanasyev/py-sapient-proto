from sapient_msg import proto_options_pb2 as _proto_options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegistrationAck(_message.Message):
    __slots__ = ("acceptance", "ack_response_reason")
    ACCEPTANCE_FIELD_NUMBER: _ClassVar[int]
    ACK_RESPONSE_REASON_FIELD_NUMBER: _ClassVar[int]
    acceptance: bool
    ack_response_reason: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, acceptance: _Optional[bool] = ..., ack_response_reason: _Optional[_Iterable[str]] = ...) -> None: ...
