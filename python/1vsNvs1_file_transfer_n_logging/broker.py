import datetime
import time
import zmq
import os

# Logging Function
def logging(transfer_status):
    with open('transfer.log', 'a') as l:
        log_message = str(datetime.now()) + ' ' + str(transfer_status) + '\n'
        l.write(log_message)

# Get file from sender and save it to temp folder
path = 'C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/tmpr'
filename = 'testfile.txt'
# Targeting file to send to receiver
destfile = path + '/' + filename
# Connect to sender and receive file
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")
receiver.setsockopt(zmq.PULL, '')
# Check if file exists
if os.path.isfile(destfile):
    transfer_status = 'success'
    time.sleep(2)
elif not os.path.isfile(destfile):
    transfer_status = 'fail'
    time.sleep(2)
# If file exists, send it to receiver and logging to "transfer.log"
if transfer_status == 'success':
    sender = context.socket(zmq.PUSH)
    sender.bind("tcp://localhost:5558")
    time.sleep(1)
    cuzFile='C:/Users/user/Desktop/Dev/GitHub/zmq_study/python/1vsNvs1_file_transfer_n_logging/tmpr/testfile.txt'
    size=os.stat(cuzFile).st_size
    target=open(cuzFile,'rb')
    file = target.read(size)
    if file:
        sender.send(file)
    os.remove(destfile)
    sender.close()
    context.term()
    target.close()
    logging('file'+' '+str(cuzFile)+' '+'Send to Receiver, success')
# If file doesn't exist, logging to "transfer.log"
elif transfer_status == 'fail':
    logging('file'+' '+str(destfile)+' '+'Send to Receiver, fail')
    context.term()