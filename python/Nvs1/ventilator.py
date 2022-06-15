# 2개의 Push 서버
import random
import sys
import asyncio
import zmq
import zmq.asyncio
ctx = zmq.asyncio.Context()
async def run_vent():
    sock_push = ctx.socket(zmq.PUSH)
    sock_push.bind('tcp://*:5556')
    sock_cmd = ctx.socket(zmq.PUSH)
    sock_cmd.connect('tcp://localhost:5557')
    input('PRESS ENTER TO START')
    amount = 1_000
    await sock_cmd.send(amount.to_bytes(4, 'big'))
    sock_cmd.close()
    for _ in range(amount):
        v = random.randrange(10, 200)
        await sock_push.send_pyobj(v)
    sock_push.close()
    input('PRESS ENTER TO QUIT')
if __name__ == '__main__':
    asyncio.run(run_vent())



    # https://soooprmx.com/%EC%98%88%EC%A0%9C-zmq-asyncio-%EB%A1%9C-push-pull-%EA%B5%AC%EC%84%B1/