"""
Name: Jayveersinh Raj
Group: BS20-DS-01
To use it use the script as in the labs: python3 client.py <ip>:<port_number>
for example: python3 client.py 127.0.0.1:5000
"""

from importlib.metadata import metadata
from re import M
from urllib import response
import grpc
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import sys
from concurrent import futures
import zlib

channel = grpc.insecure_channel(sys.argv[1])
stub = pb2_grpc.chordStub(channel)

id = 0
m = 0
fingre_table ={}

def get_finger_table_func():
      global fingre_table
      nodes = {}
      msg = pb2.populate_id(populate_id= int(id))
      response = stub.populate_finger_table(msg)
      for res in response:
       res = str(res).split('\n')
       res_1 = res[0].split(':')
       res_1 = res_1[1].replace('"', '')

       res_2 = res[1].split(' ')
       res_2 = res_2[1].replace('"', '')
       #res = res[1:]
       #res_new = [res[1], res[2]]
      #
       #res_0 = int(res[0])
       #print(f"res0 : {res_0[1:]}")
       nodes[res_1] = res_2
      
      nodes["id"] = str(id)
      fingre_table = nodes
      return nodes
     # print(nodes)
     # self.finger_table = nodes
      


 # Server starts
def start_node_server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
   pb2_grpc.add_chordServicer_to_server(NodeHandler(ip=sys.argv[2]), server)
   server.add_insecure_port(sys.argv[2])
   try:
     print("Server on")
     server.start()
     server.wait_for_termination()
   except KeyboardInterrupt:
      quit()

def quit():
      global id
      msg = pb2.id(deregister_id = int(id))
      response = stub.deregister(msg)
      print(response)
      print("Shutting the Node down...")
      
### Need to store nodes globally... ###      

class NodeHandler(pb2_grpc.chordServicer):
    def __init__(self, ip):
        super(NodeHandler, self).__init__()
        self.ip_address = ip
        #Not used yet
        self.predecessor = None, None
        self.finger_table = fingre_table
        self.text = {}
        self.m = m
        self.id = id
   

    def get_finger_table(self, request, context):
      self.finger_table = get_finger_table_func()
      for key in self.finger_table:
         yield pb2.finger_table(key = str(key), address = self.finger_table[key])
         
    #def get_finger_table(self):
     #   return self.finger_table
      
    def save(self, request, context):
       
        self.m = int(self.m)
        key = request.key
        text = request.text
        hash_value = zlib.adler32(key.encode())
        target_id = hash_value % 2 ** self.m

        return self.file_lookup(key, target_id, text)

    def successor_id(self):
        self.finger_table.pop(" Predecessor", None)
        self.finger_table.pop("id", None)
        keys = list(map(int, self.finger_table.keys()))
        for i in range(int(self.id) + 1, 2 ** self.m):
            if i in keys:
                return i
        return min(map(int, self.finger_table.keys()))

    def farthest_node(self, target_id):
        self.finger_table.pop(" Predecessor", None)
        self.finger_table.pop("id", None)
       
        index = -1
        sorted_keys = sorted(map(int, self.finger_table.keys()))
        while sorted_keys[index] <= target_id:
            index += 1
            if index == len(sorted_keys):
                break
        return sorted_keys[index - 1]

    def file_lookup(self, key_, target_id, filename):
        self.predecessor = self.finger_table[" Predecessor"]
      
        if (int(self.predecessor[0].split(':')[0]) < int(target_id) <= int(self.id) or (
               int(self.predecessor[0].split(':')[0]) > int(self.id) >= int(target_id))):
               
               if self.text.get(filename):
                return pb2.success_msg(success = False, msg = f"{filename} already exists in Node {self.id}")
               self.text[filename] = True
               print(True, f"{key_} saved in Node {self.id}")
               return pb2.success_msg(success = True, msg =f"{key_} saved in Node {self.id}")

        if (int(self.id) < target_id <= int(self.successor_id())):
         
            successor_node = self.successor_id()
            successor_rpc = self.finger_table[str(' ' + str(self.successor_id()))]

            channel = grpc.insecure_channel(successor_rpc)
            stub = pb2_grpc.chordStub(channel)
            msg = pb2.key_text(key= key_, text = filename)
            response = stub.save(msg)
            print(str(response).split('\n')[1].split(':')[1])
            if(str(response).split('\n')[0].split(':')[1].replace(' ', '') == "true"):
                return pb2.success_msg(success = True,
                                   msg = str(response).split('\n')[1].split(':')[1])
            else: 
                return pb2.success_msg(success = False,
                                   msg = str(response).split('\n')[1].split(':')[1])

            
           # return successor_rpc.savefile(filename)
        farthest = self.farthest_node(target_id)
        
        channel = grpc.insecure_channel(self.finger_table[' ' + str(farthest)])
        stub = pb2_grpc.chordStub(channel)

        msg = pb2.key_text(key= key_, text = filename)
        response = stub.save(msg)
        print(response)
        print(str(response).split('\n')[1].split(':')[1].split('\"')[2].split('\\')[0])
        if(str(response).split('\n')[0].split(':')[1].replace(' ', '') == "true"):
          return pb2.success_msg(success = True,
                                   msg = str(response).split('\n')[1].split(':')[1])
        else: 
          return pb2.success_msg(success = False,
                                   msg = str(response).split('\n')[1].split(':')[1].split('\"')[2].split('\\')[0])

        


   

            
        

if __name__ == "__main__":
    channel = grpc.insecure_channel(sys.argv[1])
    stub = pb2_grpc.chordStub(channel)

    notRegistered = True
    
    try:
          while notRegistered:
                   line = input("> ")
                   line_split = line.split()

                   arg = line_split[1:]
                   new_arg = ' '.join(arg)
                   
                   if(line_split[0] == "register"):
                     if(id != 0):
                        print("Node is already registered")

                     else:   
                        notRegistered = False
                        address = sys.argv[2]
                        address = str(address)
                        msg = pb2.address(addr=address)
                        response = stub.register(msg)

                        res = str(response)
                        print(res)
                        
                        res = str(res).split(':')
                        m = res[2].replace('"', '')
                        res = res[1]
                        print(m)
                        res = res.split()
                  
                        id = int(res[0].replace('"', ''))
                        print(id)
                        get_finger_table_func()

                        start_node_server()

    
    except KeyboardInterrupt:
          print("Turning off...")


                    