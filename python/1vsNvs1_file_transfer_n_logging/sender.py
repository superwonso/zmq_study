import zmq
import time
import os
import datetime
import hashlib

i=1

def logging(transfer_status):
    with open('transfer.log', 'a') as l:
        log_message = str(datetime.datetime.now()) + ' ' + str(transfer_status) + '\n'
        l.write(log_message)

def calc_file_hash(path):
    f = open(path, 'rb')
    data = f.read()
    hash = hashlib.md5(data).hexdigest()
    return hash

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
    filename = 'testfile2.hwp'
    curFile = path + '/' + filename
    print('File Name : ', curFile)
    size = os.stat(curFile).st_size
    print('File size:',size)
# Targeting file
    target = open(curFile, 'rb')
    file = target.read(size)
    if file:
        publisher.send(file)
    hash_val = calc_file_hash(curFile)
    logging('Sender :'+ ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Send file to broker, success')
    file = target.close()
# Take a break for re-send file
    time.sleep(1)