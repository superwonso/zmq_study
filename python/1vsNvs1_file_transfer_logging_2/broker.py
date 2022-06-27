import datetime
import time
import zmq
import os
import hashlib


# Calculate md5 checksum 'path' file
def calc_file_hash(path):
    f = open(path, 'rb')
    data = f.read()
    hash = hashlib.md5(data).hexdigest()
    return hash

# Logging Function
def logging(transfer_status):
    with open('transfer.log', 'a') as l:
        log_message = str(datetime.datetime.now()) + ' ' + str(transfer_status) + '\n'
        l.write(log_message)

# Get file from sender and save it to temp folder
path = './tmp'
filename = input('What is the file name?\n')
# Targeting file to send to receiver
destfile = path + '/' + filename
# Connect to sender and receive file
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5557")
subscriber.setsockopt(zmq.SUBSCRIBE,b'')
time.sleep(1)
msg = subscriber.recv()
if msg:
    f = open(destfile, 'wb')
    print ('open')
    f.write(msg)
    print ('close\n')
    f.close()
# Check if file exists
if os.path.isfile(destfile):
    transfer_status = 'success'
    hash_val = calc_file_hash(destfile)
    logging('Broker :' + ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Get file from Sender, success')
    time.sleep(1)
elif not os.path.isfile(destfile):
    transfer_status = 'fail'
    logging('Broker :' + ' '  + 'file :' + ' ' + str(filename) + 'Get file from Sender, fail')
    time.sleep(1)
    # If file exists, send it to receiver and logging to "transfer.log"
if transfer_status == 'success':
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5558")
    time.sleep(1)
    size=os.stat(destfile).st_size
    target=open(destfile,'rb')
    file = target.read(size)
if file:
    publisher.send(file)
    logging('Broker :' + ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Send file to Receiver, success')
    file=target.close()
    os.remove(destfile)
# If file doesn't exist, logging to "transfer.log"
elif transfer_status == 'fail':
    logging('Broker :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'Send file to Receiver, fail')
