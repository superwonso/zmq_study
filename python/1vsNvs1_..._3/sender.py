import zmq
import time
import os

i=0
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5557")

while True:
    print("Press Enter if you want to send")
    tmp = input()
    if tmp is not None :
        # Prepare context & publisher
        time.sleep(1)
        # Declare Var for file dir and file name
        path = './src'
        file_list = os.listdir(path)
        print(file_list)
        index_max = len(file_list) - 1
        if i > index_max:
            i = 0
        index = i
        i += 1
        fileloca = path + '/' + file_list[index]
        print('File Name : \n', fileloca)
        size = os.stat(fileloca).st_size
        print('File size: \n',size)
        # Targeting file
        target = open(fileloca, 'rb')
        file = target.read(size).decode('utf-8')
        if file:
            print(f"message : {fileloca} {size} {file}")
            print('\n')
            publisher.send_string(f"{fileloca} {size} {file}")
        file = target.close()
        # Take a break for re-send file
        time.sleep(1)
