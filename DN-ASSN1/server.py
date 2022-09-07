"""
@author - Parth Kalkar
To run - Download the file - open terminal in that folder -
         type "python3 server1.py port"
"""


from asyncio.windows_events import NULL
from http import client
from logging import exception
from queue import Empty
import socket
import json
import sys
import os

# clients list
clients = []

# localIP and localPort
host = socket.gethostname()
local_ip = socket.gethostbyname(host)  # localIP = "127.0.0.1"
local_port = 5000  # localPort = 20001
print("Server is on and is using UDP protocol!!")
print("Connection IP: ", local_ip)

# socket creation
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# socket binding
udp_socket.bind((local_ip, local_port))

# bufferSize
bufferSize = 1024

import binascii

# Checksum Function
def checksum(file_contents):
    file_contents = (binascii.crc32(file_contents) & 0xFFFFFFFF)
    return "%08X" % file_contents




# To check and make 'uploaded_files' directory if does not exist
def make_dir():
    if not os.path.isdir("uploaded_files"):
        os.mkdir("uploaded_files")


# To check if file exists
def exist(filename):
    return os.path.exists('./uploaded_files/'+ filename)


# Receive Function
def receive():

    # using a try - catch block to avoid any kind of exception/error
    # We will kick the client out after 20 seconds of being connected and no response
    try:
        string_data = udp_socket.recvfrom(1024)
        #if(string_data == "Connected"):
         #   udp_socket.settimeout(20.0)
          #  udp_socket.sendto("Get lost".encode(), string_data[1])
            

        file_info = json.loads(string_data[0])
        print(f"Receiving {file_info}\nby {string_data[1]}")
        udp_socket.sendto(str(bufferSize).encode(), string_data[1])
        #print("string_data: ", string_data[1][0])
        clients.append(string_data[1][0])
        
        # if(exist(file_info['name'])):
          #   udp_socket.sendto("File exists".encode(), string_data[1])


    except KeyboardInterrupt:
        sys.exit()

    # Lets check and if not existing lets create the 'uploaded_files' directory
    make_dir()


    # if the previous block is executed properly then
    # we open a new file with a corresponding name
    receive_file = open("./uploaded_files/" + file_info["name"], 'wb')

    # trying to get all the bytes in a loop
    try:
        process_is_on = True
        while process_is_on:
            next_bytes = udp_socket.recvfrom(bufferSize)
            if not next_bytes[0] == "Done".encode():
                receive_file.write(next_bytes[0])
            else:
                break

    # if an error occurs then restart
    except:
        print("Error occurred while receiving client's image. Please try again... ")
        sys.exit()

    # if everything is ok then close the file
    receive_file.close()

    # reopen it in reading mode to get its checksum
    receive_file = open("./uploaded_files/" + file_info["name"], 'rb')
    image_checksum = checksum(receive_file.read())
    file_name = file_info["name"]

    # if the checksums match then send "OK" to the client
    if image_checksum == file_info["checksum"]:
        udp_socket.sendto("OK".encode(), string_data[1])
        print(f"The file \'{file_name}\' is successfuly received, check the 'uploaded_files' folder\n")
    else:
        print(f"The checksums has not much. Earlier file removed.\n")


# start to receive until stopped
while True:
 if(udp_socket.recvfrom(1024)[0].decode("utf-8") == "Connected"):
 #   print(udp_socket.recvfrom(1024)[0].decode("utf-8"))
    receive()

  
