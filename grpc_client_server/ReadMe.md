    python3 -m grpc_tools.protoc service.proto --proto_path=. --python_out=. --grpc_python_out=.
    
use the above in the shell to create the protobuff files for server and client.

## This is a simple client server python implementation using grpc for rpc.
## Below is how to run it
    python3 client.py <ip-addr>:<port-number>
<br>    
    
    python3 server.py <port-number>
