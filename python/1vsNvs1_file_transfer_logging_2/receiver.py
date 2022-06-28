import zmq
import time
import shutil
import datetime
import os

def logging(transfer_status):
    with open('transfer.log', 'a') as l:
        log_message = str(datetime.datetime.now()) + ' ' + str(transfer_status) + '\n'
        l.write(log_message)

def file_rename(old_name, new_name):
    os.rename(old_name, new_name)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(old_name) + ' ' + 'rename to :' + ' ' + str(new_name) + ' ' + 'success')

def file_delete(file_info):
    os.remove(file_info)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(file_info) + ' ' + 'delete success')

def file_move(filename, src, dst):
    shutil.move(src + filename, dst + filename)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'move to :' + ' ' + str(dst) + ' ' + 'success')

def receive_file(filename):
    # Targeting dir for receive file
    path = './dst'
    filename = input('What is the file name?\n')
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
        print('Logging')
        logging('Receiver :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'received success')
    time.sleep(5)

def init():
    prompt = """
        1. Receive file
        2. Rename file
        3. Delete file
        4. Move file
        5. Exit
        Enter number : 
        """
    while True:
        number = 0
        print(prompt)
        number = input()
        if number == '1':
            receive_file(filename)
        elif number == '2':
            old_name = input('What is the old file name?\n')
            new_name = input('What is the new file name?\n')
            file_rename(old_name, new_name)
        elif number == '3':
            file_info = input('What is the file name?\n')
            file_delete(file_info)
        elif number == '4':
            filename = input('What is the file name?\n')
            src = input('What is the source directory?\n')
            dst = input('What is the destination directory?\n')
            file_move(filename, src, dst)
        elif number == '5':
            print('Exit')
            exit()
        else:
            print('Invalid input')
            continue

init()