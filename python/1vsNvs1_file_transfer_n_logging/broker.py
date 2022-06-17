import datetime
import time
import zmq
import os

i=1

# Logging Function
def logging(transfer_status):
    with open('transfer.log', 'a') as l:
        log_message = str(datetime.datetime.now()) + ' ' + str(transfer_status) + '\n'
        l.write(log_message)
while True:
    print(i)
    i+=1
    # Get file from sender and save it to temp folder
    path = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/tmpr'
    filename = 'testfile.txt'
    # Targeting file to send to receiver
    destfile = path + '/' + filename
    # Connect to sender and receive file
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt(zmq.SUBSCRIBE,b'')
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
        time.sleep(2)
    elif not os.path.isfile(destfile):
        transfer_status = 'fail'
        time.sleep(2)
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
        logging('file'+' '+str(destfile)+' '+'Send to Receiver, success')
    # If file doesn't exist, logging to "transfer.log"
    elif transfer_status == 'fail':
        logging('file'+' '+str(destfile)+' '+'Send to Receiver, fail')