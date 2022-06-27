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

def file_move(file_name, src, dst):
    shutil.move(src + file_name, dst + file_name)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(file_name) + ' ' + 'move to :' + ' ' + str(dst) + ' ' + 'success')

def receive_file(file_name):
    # Targeting dir for receive file
    path = './dst'
    file_name = input('What is the file name?\n')
    destfile = path + '/' + file_name
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
        logging('Receiver :' + ' ' + 'file :' + ' ' + str(file_name) + ' ' + 'received success')
    time.sleep(5)

def init(doing):
    doing = input('What do you want to do?\n1. Receive file\n2. Rename file\n3. Delete file\n4. Move file\n')
    if doing == '1':
        receive_file()
        init(doing)
    elif doing == '2':
        old_name = input('What file do you want to rename?\n')
        new_name = input('What is the new name?\n')
        file_rename(old_name, new_name)
        init(doing)
    elif doing == '3':
        file_info = input('What file do you want to delete?\n')
        file_delete(file_info)
        init(doing)
    elif doing == '4':
        file_name = input('What file do you want to move?\n')
        src = input('What is the source directory?\n')
        dst = input('What is the destination directory?\n')
        file_move(file_name, src, dst)
        init(doing)

init()