import sys
import zmq


#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from server...")
socket.connect("tcp://10.68.71.184:5556")

socket.setsockopt(zmq.SUBSCRIBE, b'')

for update_nbr in range(5):
    string = socket.recv_string()
    print string
