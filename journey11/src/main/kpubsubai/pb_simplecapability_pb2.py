# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_simplecapability.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_simplecapability.proto',
  package='journey11.kpubsubai.simple',
  syntax='proto3',
  serialized_pb=_b('\n\x19pb_simplecapability.proto\x12\x1ajourney11.kpubsubai.simple\"=\n\x12PBSimpleCapability\x12\r\n\x05_uuid\x18\x01 \x01(\t\x12\x18\n\x10_capability_name\x18\x02 \x01(\tb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PBSIMPLECAPABILITY = _descriptor.Descriptor(
  name='PBSimpleCapability',
  full_name='journey11.kpubsubai.simple.PBSimpleCapability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_uuid', full_name='journey11.kpubsubai.simple.PBSimpleCapability._uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='_capability_name', full_name='journey11.kpubsubai.simple.PBSimpleCapability._capability_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=57,
  serialized_end=118,
)

DESCRIPTOR.message_types_by_name['PBSimpleCapability'] = _PBSIMPLECAPABILITY

PBSimpleCapability = _reflection.GeneratedProtocolMessageType('PBSimpleCapability', (_message.Message,), dict(
  DESCRIPTOR = _PBSIMPLECAPABILITY,
  __module__ = 'pb_simplecapability_pb2'
  # @@protoc_insertion_point(class_scope:journey11.kpubsubai.simple.PBSimpleCapability)
  ))
_sym_db.RegisterMessage(PBSimpleCapability)


# @@protoc_insertion_point(module_scope)
