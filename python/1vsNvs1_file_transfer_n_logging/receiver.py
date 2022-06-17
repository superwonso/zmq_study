import zmq
import time

while True:
# Targeting dir for receive file
    path = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/to'
    filename = 'testfile.txt'
    destfile = path + '/' + filename
# Connect to broker and receive file
    context = zmq.Context()
    subscriber = context.socket(zmq.PULL)
    subscriber.connect("tcp://localhost:5558")
    subscriber.setsockopt(zmq.PULL,'')
    msg = subscriber.recv()
    time.sleep(5)