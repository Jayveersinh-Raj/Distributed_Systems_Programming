"""
@author - Jayveersinh Raj BS20-DS-01
To run - Download the file - open terminal in that folder -
         type "python3 server.py port"
"""


import socket
import sys
import threading
import multiprocessing

# Some useful global things
clients_q = multiprocessing.Queue()
MAX_CLIENTS = 2 # At max atleast 3 clients 6. Requirement

# exception handling for port
try:
    global server_port
    server_port = int(sys.argv[1]) # 7. Requirement
except IndexError:
    print("Usage example: python./server.py <port>")
    sys.exit()

# server_ip, buffer size and adapting connection
server_ip = "127.0.0.1"
buffer_size = 1024
server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# exception handling while binding
try:
    server_tcp_socket.bind((server_ip, server_port))
except socket.error:
    print("Error while binding to the specified port")
    sys.exit()

# server is set
print(f"Starting the server on {server_ip}:{server_port}")
server_tcp_socket.listen()


# Check for the prime number
def is_prime(n):
 n = int(n)
 if n in (2, 3):
    return "Prime"
 if n % 2 == 0:
    return "Not prime"
 for divisor in range(3, n, 2):
   if n % divisor == 0:
    return "not prime"
 return "prime"


# The main work to take the clients from queue and check the numbers, 4. Requirement
def work():
    while True:
        job = clients_q.get()
        # Accepts till connected
        connected = True
        while connected:
           number = job[0].recv(1024).decode()
           if(number == "Done"):
            connected = False
            print(f"{job[1]} disconnected")
           else:
            result = is_prime(number)
            str = "The number "+number+" is "+result
            job[0].send(str.encode())
        job[0].close()



# Function to create workers, # Statifies 3. requirement worker thread
def create_worker():

    for _ in range(MAX_CLIENTS): # Satisfies 6. requirement
        t = threading.Thread(target = work)
        t.daemon = True # free the memory once the job is done
        t.start()


# The clients handling function, 1. Completes 1st requirement
def handle_clients(conn, addr):
    create_worker()
    print(f"{addr} connected")
    clients_q.put((conn, addr))
    # clients_q.join()
    print(clients_q.get())
   
   
# The main thread that calls for the work
try:
    while True:
            print(f"Up and running!!!")
            conn, addr = server_tcp_socket.accept()

            # The main thread to handle the clients
            main_thread = threading.Thread(target = handle_clients, args=(conn,addr))
            main_thread.start()

# 5. would be covered
except KeyboardInterrupt:
    server_tcp_socket.close()
    sys.exit()