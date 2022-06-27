import zmq
import time
import os

i=1


while True:
    print(i)
    i+=1
# Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")
    time.sleep(1)
# Declare Var for file dir and file name
    path = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/from'
    filename = 'testfile.txt'
    curFile = path + '/' + filename
    print('File Name : ', curFile)
    size = os.stat(curFile).st_size
    print('File size:',size)
# Targeting file
    target = open(curFile, 'rb')
    file = target.read(size)
    if file:
        publisher.send(file)
    file = target.close()
# Take a break for re-send file
    os.system('cls')
    time.sleep(1)
    