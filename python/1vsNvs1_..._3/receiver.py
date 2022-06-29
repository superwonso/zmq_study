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
    os.rename('./dst' + '/' + old_name, './dst' + '/' + new_name)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(old_name) + ' ' + 'rename to :' + ' ' + str(new_name) + ' ' + 'success')
    print('Complete')

def file_delete(file_info):
    os.remove('./dst' + '/' + file_info)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(file_info) + ' ' + 'delete success')
    print('Complete')

def file_move(filename, src, dst):
    shutil.move('./' + src + '/' + filename, './' + dst + '/' + filename)
    logging('Receiver :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'move to :' + ' ' + str(dst) + ' ' + 'success')
    print('Complete')

def receive_file(filename, size, filememo):
    # Connect to broker and receive file
    # Targeting dir for receive file
    print("-----------------------------",filename, size, filememo)
    path = './dst'
    # filename = input('What is the file name?\n')
    # filename = filename.decode('utf-8')
    destfile = path + '/' + filename
    if msg:
        print('open')
        file = open(destfile, 'wb')
        filememo = filememo.encode()
        file.write(filememo)
        print('close\n')
        file.close()
        print('Logging')
        logging('Receiver :' + ' ' + 'file :' + ' ' + str(filename) + ' ' + 'received success')
    time.sleep(5)

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5558")
subscriber.setsockopt_string(zmq.SUBSCRIBE,'')

while True:
    msg = subscriber.recv()
    
    fileloca, size, filememo = msg.split()
    fileloca = fileloca.decode('utf-8')
    size = size.decode('utf-8')
    filememo = filememo.decode('utf-8')
    print(">>>>>>", fileloca, size, filememo)
    filename = fileloca[6:]

    print(f" file info : {fileloca}, {size}, {filememo}")

    prompt = """
    1. Receive file
    2. Rename file
    3. Delete file
    4. Move file
    5. Pass upper file
    6. Exit """
    number = 0
    print(prompt)
    number = input('Enter number : ')
    if number == '1':
        receive_file(filename, size, filememo)
        continue
    elif number == '2':
        old_name = input('2_What is the old file name?\n')
        new_name = input('2_What is the new file name?\n')
        file_rename(old_name, new_name)
        continue
    elif number == '3':
        file_info = input('3_What is the file name?\n')
        file_delete(file_info)
        continue
    elif number == '4':
        filename = input('4_What is the file name?\n')
        src = input('4_What is the source directory?\n')
        dst = input('4_What is the destination directory?\n')
        file_move(filename, './'+src, './'+dst)
        continue
    elif number == '5' :
        print('5_Pass upper file')
        pass
    elif number == '6':
        print('Exit')
        exit()
    else :
        print('Invalid number')
        pass