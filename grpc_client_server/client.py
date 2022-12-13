"""
Name: Jayveersinh Raj
Group: BS20-DS-01
To use it use the script as in the labs: python3 client.py <ip>:<port_number>
for example: python3 client.py 127.0.0.1:5000
"""

from urllib import response
import grpc
import service_pb2_grpc as pb2_grpc
import service_pb2 as pb2
import sys


if __name__ == "__main__":

    channel = grpc.insecure_channel(sys.argv[1])
    stub = pb2_grpc.serviceStub(channel)

    try:
          while True:
                   line = input("> ")
                   line_split = line.split()

                   arg = line_split[1:]
                   new_arg = ' '.join(arg)
                   
                   if(line_split[0] == "reverse"):
                     msg = pb2.inpt(inp = new_arg)
                     response = stub.reverse(msg)
                     print(response)

                   elif(line_split[0] == "split"):
                     msg = pb2.text(text = new_arg)
                     response = stub.split(msg)
                     print(response)

                   elif(line_split[0] == "isprime"):
                     for i in range (0, len(arg)):
                        arg[i] = int(arg[i])

                     msg = pb2.num(num = arg)
                     response = stub.isprime(msg)

                     for i in response.ans:
                        print(i)

                   elif(line_split[0] == "exit"):
                      print("Shutting down")
                      sys.exit(0)

    
    except KeyboardInterrupt:
                print("Turning off...")


                    