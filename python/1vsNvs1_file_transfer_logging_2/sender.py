import zmq
import time
import os

def Run_sender():
    # Prepare context & publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")
    time.sleep(1)
    # Declare Var for file dir and file name
    path = './src'
    filename = input('What is the file name?\n')
    curFile = path + '/' + filename
    print('File Name : \n', curFile)
    size = os.stat(curFile).st_size
    print('File size: \n',size)
    # Targeting file
    target = open(curFile, 'rb')
    file = target.read(size)
    if file:
        publisher.send(file)
    file = target.close()
    # Take a break for re-send file
    time.sleep(1)

def init(doing):
    if doing == '0' : 
        doing = input('What do you want to do?\n1. Run Sender\n2. Exit\n')
        if doing == '1':
            Run_sender()
            doing == '0'
            init(doing)
        elif doing == '2':
            print('Exit')
            exit()

doing = 0
init(doing)
