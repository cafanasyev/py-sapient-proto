"""Every generated module must import cleanly."""
import importlib

import pytest

V2_MODULES = [
    "alert_pb2",
    "alert_ack_pb2",
    "associated_detection_pb2",
    "associated_file_pb2",
    "detection_report_pb2",
    "error_pb2",
    "follow_pb2",
    "location_pb2",
    "range_bearing_pb2",
    "registration_pb2",
    "registration_ack_pb2",
    "sapient_message_pb2",
    "status_report_pb2",
    "task_pb2",
    "task_ack_pb2",
    "velocity_pb2",
]


def test_proto_options_imports() -> None:
    importlib.import_module("sapient_msg.proto_options_pb2")


@pytest.mark.parametrize("module", V2_MODULES)
def test_v2_module_imports(module: str) -> None:
    importlib.import_module(f"sapient_msg.bsi_flex_335_v2_0.{module}")
