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

def init(doing):
    if doing == '0':
        doing = input('What do you want to do?\n1. Receive file\n2. Rename file\n3. Delete file\n4. Move file\n5. Exit\n')
        if doing == '1':
            receive_file()
            doing == '0'
            init(doing)
        elif doing == '2':
            old_name = input('What file do you want to rename?\n')
            new_name = input('What is the new name?\n')
            file_rename(old_name, new_name)
            doing == '0'
            init(doing)
        elif doing == '3':
            file_info = input('What file do you want to delete?\n')
            file_delete(file_info)
            doing == '0'
            init(doing)
        elif doing == '4':
            filename = input('What file do you want to move?\n')
            src = input('What is the source directory?\n')
            dst = input('What is the destination directory?\n')
            file_move(filename, src, dst)
            doing == '0'
            init(doing)
        elif doing == '5':
            print('Bye')
            exit()

doing = 0
init()