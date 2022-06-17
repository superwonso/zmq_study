import zmq
import time

i=1

while True:
    print(i)
    i+=1
# Targeting dir for receive file
    path = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/to'
    filename = 'testfile.txt'
    destfile = path + '/' + filename
# Connect to broker and receive file
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5558")
    subscriber.setsockopt(zmq.SUBSCRIBE,b'')
    msg = subscriber.recv()
    if msg:
        f = open(destfile, 'wb')
        print('open')
        f.write(msg)
        print('close\n')
        f.close()
    time.sleep(5)