"""
Name: Jayveersinh Raj
Group: BS20-DS-01
To use it use the script as in the labs: python3 client.py <ip>:<port_number>
for example: python3 client.py 127.0.0.1:5000
"""

from asyncio.windows_events import NULL
from queue import Empty
from urllib import request, response
import grpc
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import sys


if __name__ == "__main__":
    connected = False
    isRegistry = False
    isNode = False
    id = 0
    notQuit = True
    try:
          while notQuit:
                   line = input("> ")
                   line_split = line.split()

                   arg = line_split[1:]
                   new_arg = ' '.join(arg)
                   
                   if(line_split[0] == "connect"):
                     finger_table = []
                     if(len(line_split) == 2):
                       channel = grpc.insecure_channel(line_split[1])
                       stub = pb2_grpc.chordStub(channel)
                       
                       try:
                         empty = pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                         response = stub.get_chord_info(empty)
                       
                         for res in response:
                            res = str(res).split(':')
   
                         connected = True
                         isRegistry = True
                         isNode = False

                       except grpc.RpcError as e:
                         connected = False
                         isRegistry = False
                         pass

                      
                       if(not isRegistry):
                        try:
                           empty = pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                           response = stub.get_finger_table(empty)
                        
                           for res in response:
                         
                            res = str(res).split('\n')
                            res_id = res[0].split(':')
                            res_id = res_id[1]
  
                            res_addr = res[1].split(':')
                            res_addr = res_addr[1:]
                            res_addr = ':'.join(res_addr)
  
                            ft = res_id + res_addr
                            finger_table.append(ft)
      
                           if(len(finger_table)!=0):
                              id = finger_table[-1].split()[1]
                           
                           connected = True
                           isNode = True

                        except grpc.RpcError as e:
                         connected = False
                         isNode = False
                         pass

                     else:
                        pass
                     
                     if(isRegistry):
                        print("connected to registry")
                     
                     elif(isNode):
                        print("connected to Node " + id.replace('"', ''))
                      # elif(hasattr(stub, 'get_finger_table')):
                      #  print("Connected to a Node")
                      #  connected = True
                      
                     else:
                        pass
                     

                   elif(line_split[0] == "get_info"):
                     if(connected and isRegistry):
                        empty = pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                        response = stub.get_chord_info(empty)
                        for res in response:
                            res = str(res).split(':')
                            res = res[1:]
                            res_new = ':'.join(res).strip('"')
                            print(res_new)

                     elif(connected and isNode):
                         empty = pb2.google_dot_protobuf_dot_empty__pb2.Empty()
                         response = stub.get_finger_table(empty)
                         finger_table = []
                         for res in response:
                          #finger_table.append(res)
                          #print(res) 
                          res = str(res).split('\n')
                          res_id = res[0].split(':')
                          res_id = res_id[1]

                          res_addr = res[1].split(':')
                          res_addr = res_addr[1:]
                          res_addr = ':'.join(res_addr)

                          ft = res_id + res_addr
                          finger_table.append(ft)
                          f_table = finger_table[:-1]
                          for ft in f_table[:-1]:
                           ft = ft.replace('"', '')
                           ft = ft.replace('  ', '')
                           ft = ft.replace(' ', ': ')
                           print(ft)
                           
                         pred = finger_table[-2].replace('"', '')
                         pred = pred.split()

                         pred_addr = pred[1].split(':')
                         pred_addr_ip = ':'.join([pred_addr[1], pred_addr[2]])
                         pred_addr = pred_addr[0] + ":" + ' ' + pred_addr_ip
                         #pred = pred.replace(' ', '')
                         print(pred[0] + ' ' + pred_addr)
                     else:
                         pass

                     #response = stub.split(msg)
                     #print(response)
                   elif(connected and isNode and line_split[0] == "save"):
                     key = line[2:].split('"')
                     if(len(key) > 1):
                        text_ = ' '.join(key[2:])
                        msg = pb2.key_text(key= key[1], text = text_)
                        response = stub.save(msg)
                        
                        if(len(str(response).split('\n'))<3):
                           print(f"false {str(response).split(':')[1]}")
                        
                        else:
                           res_0 = str(response).split('\n')[0].split(':')[1]
                           res_1 = str(response).split('\n')[1].split(':')[1]
                           res_1 = str(res_1).replace('\\', '')
                           res_1 = str(res_1).replace('"', '')
                           print(f"{res_0}:{res_1}")
                     else:
                        print("Please type only key within quotations " " ")
                     

                   elif(connected and isNode and line_split[0] == "find"):
                     key = line[2:].split('"')
                     if(len(key) > 1):
                        text_ = ' '.join(key[2:])
                        msg = pb2.key_text(key= key[1], text = text_)
                        response = stub.find(msg)
                        
                        if(len(str(response).split('\n'))<3):
                           print(f"false {str(response).split(':')[1]}")
                        
                        else:
                           res_0 = str(response).split('\n')[0].split(':')[1]
                           res_1 = str(response).split('\n')[1].split(':')[1]
                           res_1 = str(res_1).replace('\\', '')
                           res_1 = str(res_1).replace('"', '')
                           print(f"{res_0}:{res_1}")
                     else:
                        print("Please type only key within quotations " " ")


                   elif(line_split[0] == "quit"):
                     notQuit = False

    
    except KeyboardInterrupt:
                print("Turning off...")


                    