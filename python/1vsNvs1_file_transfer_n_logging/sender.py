import zmq
import time
import os

while True:
    msg = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/from/testfile.txt'
# Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PULL)
    publisher.bind("tcp://localhost:5557")
    time.sleep(1)
# Declare Var for file dir and file name
    curFile = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/from/testfile.txt'
    size = os.stat(curFile).st_size
    print('File size:',size)
# Targeting file
    target = open(curFile, 'rb')
    file = target.read(size)
    if file:
        publisher.send(file)
# Once file is sent, close the socket
    publisher.close()
    context.term()
    target.close()
# Take a break for re-send file
    time.sleep(10)