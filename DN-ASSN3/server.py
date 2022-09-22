"""

"""

# Importing dependencies
import socket
import sys
from unittest import result
import zmq

# Initailising ports
ports = sys.argv

# zmq initialization for inputs and outputs
context = zmq.Context()

''' For clients '''

# Input socket (Replier (rep))
sock_rep = context.socket(zmq.REP)

# Output socket (Publisher (pub))
sock_cli_pub = context.socket(zmq.PUB)


''' For workers'''

# Input socket (Replier (rep))
sock_work_pub = context.socket(zmq.PUB)

# Output socket (Publisher (pub))
sock_work_sub = context.socket(zmq.SUB)


# we bind the sockets, as a server
sock_rep.bind(f"tcp://127.0.0.1:{ports[1]}")
sock_cli_pub.bind(f"tcp://127.0.0.1:{ports[2]}")
sock_work_pub.bind(f"tcp://127.0.0.1:{ports[3]}")
sock_work_sub.bind(f"tcp://127.0.0.1:{ports[4]}")
sock_work_sub.setsockopt_string(zmq.SUBSCRIBE, '')

sock_work_sub.RCVTIMEO = 1000

while True:
    print("Up and running...!!!")
    #  Wait for next request from client
    message = sock_rep.recv_string()
    print(f"Message from {sock_rep}:", message)
    sock_rep.send_string("Recieved")
    
    # sock_cli_pub.send_string(message)
    
    if(message.split()[0] == "isprime" or message.split()[0] == "gcd"):
       sock_work_pub.send_string(message)
       # sock_cli_pub.send_string(message.decode('utf-8'))
       output = sock_work_sub.recv_string()
       sock_cli_pub.send_string(output)
     
    else:
     sock_cli_pub.send_string(message)
    
    





