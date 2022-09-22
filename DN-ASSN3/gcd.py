"""

"""

# Importing dependences
import sys
import zmq
import math


# Initailising ports
ports = sys.argv

# zmq initialization for inputs and outputs
context = zmq.Context()

# Requesting socket (input)
sock_pub = context.socket(zmq.PUB)

# Subscribing socket (output)
sock_sub = context.socket(zmq.SUB)

# Lets connect the socket now
sock_sub.connect(f"tcp://127.0.0.1:{ports[1]}")
sock_pub.connect(f"tcp://127.0.0.1:{ports[2]}")
sock_sub.setsockopt_string(zmq.SUBSCRIBE, '')

# set a timeout for receive, make it non-blocking
sock_sub.RCVTIMEO = 1000

# gcd function returning the result
def gcd(n1, n2):
    gcd = math.gcd(n1, n2)
    result = "gcd for " + str(n1) + " " + str(n2) + " is " + str(gcd)
    return result

try:
    while True:
           
            try:
                while True:
                   command = sock_sub.recv_string()
                   print(command)
                   split_command = command.split()
                   print(len(split_command))
                   # print(isinstance(int(number), int))
                   if (split_command[0] == "gcd" and len(split_command) < 4):
                    if(split_command[1].isdecimal() and split_command[2].isdecimal()):
                      result = gcd(int(split_command[1]), int(split_command[2]))
                      sock_pub.send_string(command + "\n" + result)
                      print(result)
                    else:
                      sock_pub.send_string("The correct format is 'gcd N n' where 'N', 'n' is are numbers ")

                   elif(split_command[0] == "isprime"):
                      pass

                   elif(len(split_command) > 3):
                      sock_pub.send_string(command)
                   

            except zmq.Again:
                pass 
            
                         
# 5. would be covered
except KeyboardInterrupt:
    print("Terminating client")
    sys.exit(0)

