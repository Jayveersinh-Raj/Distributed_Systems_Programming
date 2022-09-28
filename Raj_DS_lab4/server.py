"""
Name: Jayveersinh Raj
Group: BS20-DS-01
To use it use the script as in the labs: python3 server.py <port_number>
For example: python3 server.py 5000
"""

from concurrent import futures
import grpc
import service_pb2_grpc as pb2_grpc
import service_pb2 as pb2
import sys

class ServiceHandler(pb2_grpc.serviceServicer):
    def reverse(self, request, context):
        inpt = request.inp
        reply = inpt[::-1]
        return pb2.reverse_input(reverse_input = reply)

    def split(self, request, context):
        text = request.text
        output = text.split()
        n_parts = len(output)
        reply = {"number": n_parts, "parts" : output}
        return pb2.parts(**reply)

    def isprime(self, request, context):
        inpt = request.num
        res = []
        for n in inpt: 
                n = int(n)
                if n in (2, 3):
                   res.append(str(n) + " is prime")
        
                elif n % 2 == 0:
                   res.append(str(n) + " is not prime") 
                
                else:
                  flow_flag = 0
                  for divisor in range(3, n, 2):
                    if n % divisor == 0 and flow_flag == 0:
                       flow_flag = flow_flag + 1
                       res.append(str(n) + " is not prime")

                  if flow_flag == 0:
                       res.append(str(n) + " is Prime")

        return pb2.ans(ans = res)


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    pb2_grpc.add_serviceServicer_to_server(ServiceHandler(), server)
    server.add_insecure_port("127.0.0.1:"+ sys.argv[1])
    server.start()
    try:
        print("Server started")
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting the system down")
