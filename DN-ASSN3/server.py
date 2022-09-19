"""

"""

# Importing dependencies
import socket
import sys
import zmq

# Initailising ports
ports = sys.argv

# zmq initialization for inputs and outputs
context = zmq.Context()

# Input socket (Replier (rep))
sock_rep = context.socket(zmq.REP)

# Output socket (Publisher (pub))
sock_pub = context.socket(zmq.PUB)


# we bind the sockets, as a server
sock_rep.bind(f"tcp://127.0.0.1:{ports[1]}")
sock_pub.bind(f"tcp://127.0.0.1:{ports[2]}")


while True:
    print("Up and running...!!!")
    #  Wait for next request from client
    message = sock_rep.recv_string()
    print(f"Message from {sock_rep}:", message)
    sock_rep.send_string("Recieved")
    #  Do some 'work'

    #  Send reply back to client
    sock_pub.send_string(message)
    # sock_pub.send_string(message.decode('utf-8'))





