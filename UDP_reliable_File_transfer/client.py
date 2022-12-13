"""
@author -Jayveersinh Raj
To run - Download the file - open terminal in that folder -
         type "python3 client1.py ip_address port"
** Make sure that the server1.py is running before running this file **
** Also, make sure you have innopolis.jpg or any file that you wanna send in the same folder **
"""

import binascii
import os
import socket
import json
import sys
import time

# Local machine name, localIP and localPort
host = socket.gethostname()  # Get local machine name
local_ip = socket.gethostbyname(host)  
local_port = int(sys.argv[2]) 


# Checksum Function
def checksum(file_contents):
    file_contents = (binascii.crc32(file_contents) & 0xFFFFFFFF)
    return "%08X" % file_contents


# Exit Function
def exit():
    for i in range(10):
        print(f"Shutting down in {10 - i}...", end = "\r")
        time.sleep(5)
    sys.exit()


# Json Converter
def json_converter(file_data):
    return file_data.toJSON()



# server address - serverIP & serverPort
server_address = (local_ip, local_port)

# UDP socket creation
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Count variable to count the number of tries
count = 0


# Send Function
def sendfile():
    
    # open file
    print(f"Enter filename (from the same folder) with extension\n> ", end="")
    file = open(input(), 'rb')
    file_checksum = checksum(file.read())
    file.seek(0, os.SEEK_END)
    
    
    # fill dictionary fields
    file_info = {
        'name': file.name, 
        'size': file.tell(),
        'checksum': file_checksum
        }
    
    file.close()

    # convert to json and send
    data = json.dumps(file_info, default=json_converter, indent=2)
    udp_socket.sendto(data.encode(), server_address)
    global count
    # get the bufferSize within a second
    try:
        udp_socket.settimeout(1.0)
        bufferSize = udp_socket.recvfrom(32)
        udp_socket.settimeout(None)
    
    # if time surpasses then shut down
    except socket.timeout:
        print("Error: Timeout")
        udp_socket.close()
        exit()

    # if message received is not bufferSize then shut down
    if not str(json.loads(bufferSize[0])).isnumeric():
        print("Server Error")
        udp_socket.close()
        exit()

    bufferSize_int = int(json.loads(bufferSize[0]))

    # open file to send
    file_to_send = open(file_info['name'], "rb")

    # traverse until data can be sent
    while next_byte := file_to_send.read(bufferSize_int):
        udp_socket.sendto(next_byte, server_address)

    # inform the server when done
    udp_socket.sendto("Done".encode(), server_address)

    # try to get the "OK" message within one second
    try:
        udp_socket.settimeout(1.0)
        message = udp_socket.recvfrom(32)
        udp_socket.settimeout(None)
        
        if message[0] == "OK".encode():
            print("The file has been uploaded successfully :)")
            exit()
        
        if message[0] == "File exists".encode():
            print("The file already exists, please upload a different file")

        if message[0] == "Get lost".encode():
            exit()

        # if we didnt receive OK then repeat
        else:
            print("Something went wrong, server error")

    # if time exceeds then shut down
    except socket.timeout:
        print("Server Error ")
        udp_socket.close()
        exit()


# start to send
for i in range(5):
  udp_socket.sendto("Connected".encode(), server_address)
  sendfile()
  
