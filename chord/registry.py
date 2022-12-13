import bisect
from concurrent import futures
import random
from urllib import request
import grpc
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import sys

def successor_(id_, sorted_ids):
    try:
        return sorted_ids[bisect.bisect_left(sorted_ids, id_)]
    except IndexError:
        return sorted_ids[0]


def predecessor_(id_, sorted_ids):
    try:
        return sorted_ids[bisect.bisect_left(sorted_ids, id_) - 1]
    except IndexError:
        return sorted_ids[-1]

class RegistryHandler(pb2_grpc.chordServicer):
    def __init__(self, m, ip, port):
        super(RegistryHandler, self).__init__()
        self.ports = {}
        self.m = m
        self.ip_address = ip
        self.port = port

    def get_chord_info(self, request, context):
        for key in self.ports:
            yield pb2.nodes_list(address = f"{key} : {self.ports[key]}")


    def register(self, request, context):
        addr = request.addr
        random.seed(0)
        if len(self.ports) == 2 ** int(self.m):
            return -1, "Chord is full."

        id_ = str(random.randint(0, 2 ** int(self.m) - 1))

        while id_ in self.ports:
            id_ = str(random.randint(0, 2 ** int(self.m) - 1))

        self.ports[str(id_)] = str(addr)
        return pb2.assigned(id = str(id_), m = str(self.m))

    def deregister(self, request, context):
        id_ = request.deregister_id
        id_ = str(id_)
        if self.ports.get(id_) is None:
            return pb2.msg(success = False, message = f"Node {id_} is not part of the network")
        port = self.ports[id_]
        self.ports.pop(str(id_), None)
        return pb2.msg(success = True, message = f"Node {id_}  with  address {port}  was successfully removed")


    def populate_finger_table(self, request, context):
        self.m = int(self.m)
        id_ = request.populate_id
        finger_table = {}
        sorted_ids = sorted(map(int, self.ports.keys()))
     
        for i in range(1, self.m + 1):
            successor = successor_((int(id_) + 2 ** (i - 1)) % 2 ** self.m, sorted_ids)       
            finger_table[str(successor)] = self.ports[str(successor)]

        predecessor = str(predecessor_(int(id_), sorted_ids))
        pred = str(predecessor)
        pred_addr = self.ports[str(predecessor)]
        
        finger_table["Predecessor"] = ":".join([pred, pred_addr])
        unique_ft = dict(list(finger_table.items())[len(finger_table)//2:])
        for key in unique_ft:
            yield pb2.finger_table(key = key, address = unique_ft[key])                           
       

    def exit_process(self):
        if self.xmlrpc_server is not None:
            self.xmlrpc_server.quit = 1


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 20))
    pb2_grpc.add_chordServicer_to_server(RegistryHandler(m=sys.argv[2], ip="127.0.0.1", port= sys.argv[1]), server)
    server.add_insecure_port("127.0.0.1:"+ sys.argv[1])
    server.start()
    try:
        print("Server started")
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting the system down")