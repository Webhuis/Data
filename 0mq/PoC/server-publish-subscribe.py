import time
import zmq

# Prepare our context and publisher socket
ctx = zmq.Context()
publisher = ctx.socket(zmq.PUB)

publisher.bind("tcp://10.68.71.184:5556")

time.sleep(2)

sequence = 0
id = 0
data =1000

while sequence < 20:
  id += 1;
  data += 1000;
  publisher.send("%i %i %i" % (sequence, id, data));
  sequence += 1
