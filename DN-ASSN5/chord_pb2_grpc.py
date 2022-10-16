# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chord_pb2 as chord__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class chordStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.register = channel.unary_unary(
                '/chord/register',
                request_serializer=chord__pb2.address.SerializeToString,
                response_deserializer=chord__pb2.assigned.FromString,
                )
        self.deregister = channel.unary_unary(
                '/chord/deregister',
                request_serializer=chord__pb2.id.SerializeToString,
                response_deserializer=chord__pb2.msg.FromString,
                )
        self.populate_finger_table = channel.unary_stream(
                '/chord/populate_finger_table',
                request_serializer=chord__pb2.populate_id.SerializeToString,
                response_deserializer=chord__pb2.finger_table.FromString,
                )
        self.get_chord_info = channel.unary_stream(
                '/chord/get_chord_info',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.nodes_list.FromString,
                )
        self.get_finger_table = channel.unary_stream(
                '/chord/get_finger_table',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=chord__pb2.finger_table.FromString,
                )
        self.save = channel.unary_unary(
                '/chord/save',
                request_serializer=chord__pb2.key_text.SerializeToString,
                response_deserializer=chord__pb2.success_msg.FromString,
                )


class chordServicer(object):
    """Missing associated documentation comment in .proto file."""

    def register(self, request, context):
        """For registry
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deregister(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def populate_finger_table(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_chord_info(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_finger_table(self, request, context):
        """For nodes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def save(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_chordServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=chord__pb2.address.FromString,
                    response_serializer=chord__pb2.assigned.SerializeToString,
            ),
            'deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.deregister,
                    request_deserializer=chord__pb2.id.FromString,
                    response_serializer=chord__pb2.msg.SerializeToString,
            ),
            'populate_finger_table': grpc.unary_stream_rpc_method_handler(
                    servicer.populate_finger_table,
                    request_deserializer=chord__pb2.populate_id.FromString,
                    response_serializer=chord__pb2.finger_table.SerializeToString,
            ),
            'get_chord_info': grpc.unary_stream_rpc_method_handler(
                    servicer.get_chord_info,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=chord__pb2.nodes_list.SerializeToString,
            ),
            'get_finger_table': grpc.unary_stream_rpc_method_handler(
                    servicer.get_finger_table,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=chord__pb2.finger_table.SerializeToString,
            ),
            'save': grpc.unary_unary_rpc_method_handler(
                    servicer.save,
                    request_deserializer=chord__pb2.key_text.FromString,
                    response_serializer=chord__pb2.success_msg.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chord', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class chord(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chord/register',
            chord__pb2.address.SerializeToString,
            chord__pb2.assigned.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chord/deregister',
            chord__pb2.id.SerializeToString,
            chord__pb2.msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def populate_finger_table(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chord/populate_finger_table',
            chord__pb2.populate_id.SerializeToString,
            chord__pb2.finger_table.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_chord_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chord/get_chord_info',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            chord__pb2.nodes_list.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_finger_table(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/chord/get_finger_table',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            chord__pb2.finger_table.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def save(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chord/save',
            chord__pb2.key_text.SerializeToString,
            chord__pb2.success_msg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
