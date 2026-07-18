#!/usr/bin/env python3
"""Regenerate sapient_msg protobuf modules and type stubs from proto/.

Run with: uv run python scripts/generate.py
Requires dev dependencies (grpcio-tools, mypy-protobuf) — install with `uv sync`.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

try:
    from grpc_tools import protoc
except ImportError:
    sys.exit("grpcio-tools is not installed - run `uv sync` first")

if shutil.which("protoc-gen-mypy") is None:
    sys.exit("protoc-gen-mypy not on PATH - run `uv sync` and use `uv run`")

ROOT = Path(__file__).resolve().parent.parent
PROTO_DIR = ROOT / "proto"
OUT_DIR = ROOT / "src"
WELL_KNOWN = Path(protoc.__file__).parent / "_proto"


def main() -> int:
    protos = sorted(str(p) for p in PROTO_DIR.rglob("*.proto"))
    if not protos:
        sys.exit(f"no .proto files found under {PROTO_DIR}")
    OUT_DIR.mkdir(exist_ok=True)
    rc = protoc.main(
        [
            "protoc",
            f"--proto_path={PROTO_DIR}",
            f"--proto_path={WELL_KNOWN}",
            f"--python_out={OUT_DIR}",
            f"--mypy_out={OUT_DIR}",
            *protos,
        ]
    )
    if rc != 0:
        return rc
    sapient_msg_dir = OUT_DIR / "sapient_msg"
    pkg_dirs = {sapient_msg_dir} | {p.parent for p in sapient_msg_dir.rglob("*_pb2.py")}
    for pkg in pkg_dirs:
        (pkg / "__init__.py").touch()
    (sapient_msg_dir / "py.typed").touch()
    print(f"generated {len(protos)} protos into {OUT_DIR}/sapient_msg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
