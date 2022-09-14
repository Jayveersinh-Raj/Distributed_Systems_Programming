"""
@author - Jayveersinh Raj BS20-DS-01
To run - Download the file - open terminal in that folder -
         type "python3 client.py ip-addr:port-number"
         Example: : python3 client.py 127.0.0.1:5555
"""

import sys
import socket
import time

# Taking address and spliting it from ':'
try:
   address = sys.argv[1]
   server_ip = address.split(':')[0]
   server_port = int(address.split(':')[1])
   time_count = time.perf_counter()
except Exception as e:
    print(e)
    print("Invalid server and port arguments.\nUsage example: python ./client.py <address> <port>")
    exit(0)

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
try:
    sock.settimeout(3)
    sock.connect((server_ip, server_port))
except ConnectionError:
    print("Server is unavailable.")
    exit(0)


while True:
    try:
        print(f"Connected to : {(server_ip, server_port)}")
        numbers = [15492781, 15492787, 15492803, 
                15492811, 15492810, 15492833, 
                15492859, 15502547, 15520301, 
                15527509, 15522343, 1550784]

        for i in numbers:
          n = str(i)
          sock.send(n.encode())
          msg = sock.recv(1024).decode()
          print(msg)
        
        completed = "Done"
        print("Completed")
        sock.send(completed.encode())
        if msg in ["Sorry, will take time"] or "ERROR" in msg:
            sock.close()
            exit(0)
        response = input("> ")
        sock.send(response.encode())

    except KeyboardInterrupt:
        print("Exiting client ...")
        sock.close()
        exit(0)
        
    except ConnectionError:
        print("Connection with server lost. Exiting ...")
        sock.close()
        exit(0)
