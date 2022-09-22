"""

"""

# Importing dependencies
import sys
import zmq

# Initailising ports
ports = sys.argv

# zmq initialization for inputs and outputs
context = zmq.Context()

# Requesting socket (input)
sock_req = context.socket(zmq.REQ)

# Subscribing socket (output)
sock_sub = context.socket(zmq.SUB)

# Lets connect the socket now
sock_req.connect(f"tcp://127.0.0.1:{ports[1]}")
sock_sub.connect(f"tcp://127.0.0.1:{ports[2]}")
sock_sub.setsockopt_string(zmq.SUBSCRIBE, '')

# Timeouts
sock_sub.RCVTIMEO = 1000
sock_req.RCVTIMEO = 1000



try:
    while True:
           
            try:
                while True:
                   line = input("> ")
                   if len(line) != 0:
                    sock_req.send_string(line)
                    # sock_req.RCVTIMEO = 1000 # in milliseconds
                    msg = sock_req.recv_string()
                   print(sock_sub.recv().decode('utf-8')) 
                  
                   
                   

            except zmq.Again:
                pass 

            except zmq.ZMQError as exc:
                print("There is an error, make sure server, and/or its workers work correctly! \n")
                sys.exit(0)
            
                         
# 5. would be covered
except KeyboardInterrupt:
    print("Terminating client")
    sys.exit(0)

