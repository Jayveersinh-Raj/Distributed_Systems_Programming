This repo. conatains "Distributed Systems Programming" course assignments from batch 2022 3rd year. Innopolis University. Use the following for grpc to get server and client files from proto. Replace `chord.proto` in the following with the respective name for the proto file.

    python3 -m grpc_tools.protoc chord.proto --proto_path=. --python_out=. --grpc_python_out=.
