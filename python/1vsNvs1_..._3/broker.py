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


while True:
    # Connect to sender
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt_string(zmq.SUBSCRIBE,'')
    time.sleep(1)
    msg = subscriber.recv()
    fileloca, size, filememo = msg.split()
    filename = fileloca[6:].decode('utf-8')
    size = size.decode('utf-8')
    str(filememo)
    
    # Get file from sender and save it to temp folder
    path = './tmp'
    
    # Targeting file to send to receiver
    destfile = path + '/' + filename
    
    # Receiving file
    if msg:
        f = open(destfile, 'wb')
        print ('open')
        f.write(filememo)
        print ('close\n')
        f.close()
    
    # Check that file exists
    if os.path.isfile(destfile):
        transfer_status = 'success'
        hash_val = calc_file_hash(destfile)
        logging('Broker :' + ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Get file from Sender, success')
        time.sleep(1)
    elif not os.path.isfile(destfile): # If file exists, send it to receiver and logging to "transfer.log"
        transfer_status = 'fail'
        logging('Broker :' + ' '  + 'file :' + ' ' + str(filename) + 'Get file from Sender, fail')
        time.sleep(1)

    if transfer_status == 'success':
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.bind("tcp://*:5558")
        time.sleep(1)
        size=os.stat(destfile).st_size
        target=open(destfile,'rb')
        file = target.read(size)
        file = file.decode('utf-8')
    elif transfer_status == 'fail': 
        logging('Broker :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'Send file to Receiver, fail')
    # If file doesn't exist, logging to "transfer.log"
    if file:
        print(f" file info : {destfile}, {size}, {file}")
        publisher.send_string(f"{destfile} {size} {file}")
        logging('Broker :' + ' ' + 'file :' + ' ' + str(filename)+ ' ' + 'md5 Checksum :' + ' ' + str(hash_val) + ' ' + 'Send file to Receiver, success')
        file=target.close()
        os.remove(destfile)