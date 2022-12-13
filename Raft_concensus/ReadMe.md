    python3 -m grpc_tools.protoc raft.proto --proto_path=. --python_out=. --grpc_python_out=.
    
use the above in the shell to create the protobuff files for server and client.

## This is the implementation of raft concensus algorithm in python using grpc
