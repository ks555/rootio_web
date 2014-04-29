import zmq
import time
import random

port = "5556"
pattern = "PUB"

context = zmq.Context()
socket = context.socket(getattr(zmq,pattern))
socket.bind("tcp://*:%s" % port)
print "publish on %s as %s" % (port, pattern)

# Ensure subscriber connection has time to complete
time.sleep(1)

messages = ['hi', 'hello', 'how are you?']

while True:
    try:
        topic = random.randint(0,3)
        msg = random.choice(messages)
        print "%s: %s" % (topic, msg)
        socket.send_multipart([b"%d" % topic, b"%s" % msg])
        time.sleep(1)

    except KeyboardInterrupt:
        print "goodbye"
        break