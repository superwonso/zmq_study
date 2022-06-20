import zmq
import time
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
        file = open(destfile, 'wb')
        print('open')
        file.write(msg)
        print('close\n')
        file.close()
        hash_val = calc_file_hash(destfile)
        logging('Receiver :'+ ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Get file from broker, success')
    else :
        logging('Receiver :'+ ' ' + 'file :' + ' ' + str(filename)+ ' ' + str(hash_val) + ' ' + 'Get file from broker, fail')
    time.sleep(5)