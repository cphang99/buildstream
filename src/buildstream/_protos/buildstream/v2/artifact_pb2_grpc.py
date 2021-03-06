# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from buildstream._protos.buildstream.v2 import artifact_pb2 as buildstream_dot_v2_dot_artifact__pb2


class ArtifactServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetArtifact = channel.unary_unary(
        '/buildstream.v2.ArtifactService/GetArtifact',
        request_serializer=buildstream_dot_v2_dot_artifact__pb2.GetArtifactRequest.SerializeToString,
        response_deserializer=buildstream_dot_v2_dot_artifact__pb2.Artifact.FromString,
        )
    self.UpdateArtifact = channel.unary_unary(
        '/buildstream.v2.ArtifactService/UpdateArtifact',
        request_serializer=buildstream_dot_v2_dot_artifact__pb2.UpdateArtifactRequest.SerializeToString,
        response_deserializer=buildstream_dot_v2_dot_artifact__pb2.Artifact.FromString,
        )


class ArtifactServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetArtifact(self, request, context):
    """Retrieves an Artifact message

    Errors:
    * `NOT_FOUND`: Artifact not found on server
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateArtifact(self, request, context):
    """Sets an Artifact message

    Errors:
    * `FAILED_PRECONDITION`: Files specified in upload aren't present in CAS
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ArtifactServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetArtifact': grpc.unary_unary_rpc_method_handler(
          servicer.GetArtifact,
          request_deserializer=buildstream_dot_v2_dot_artifact__pb2.GetArtifactRequest.FromString,
          response_serializer=buildstream_dot_v2_dot_artifact__pb2.Artifact.SerializeToString,
      ),
      'UpdateArtifact': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateArtifact,
          request_deserializer=buildstream_dot_v2_dot_artifact__pb2.UpdateArtifactRequest.FromString,
          response_serializer=buildstream_dot_v2_dot_artifact__pb2.Artifact.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'buildstream.v2.ArtifactService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
