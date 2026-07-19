# cafanasyev-sapient-pydantic

SAPIENT (BSI Flex 335 v2.0) messages as hand-written
[pydantic](https://docs.pydantic.dev) models: idiomatic construction with
real, correctly-typed protobuf enums, ICD-aware validation (UUID/ULID
formats at construction; mandatory-field checks at conversion), and
bidirectional conversion to/from the google-protobuf classes shipped by
[cafanasyev-sapient-proto](https://github.com/cafanasyev/py-sapient-proto)
(pulled in automatically).

```python
from sapient_msg_pydantic.bsi_flex_335_v2_0.registration import Registration

reg = Registration(name="radar-1")
pb = reg.to_pb2()                     # model -> google-protobuf (ICD-checked)
back = Registration.from_pb2(pb)      # google-protobuf -> model (validated)
```

See the [repository](https://github.com/cafanasyev/py-sapient-proto) for
details and licensing (proto definitions are Dstl (c) Crown Copyright 2024,
implementing BSI Flex 335 © The British Standards Institution).
