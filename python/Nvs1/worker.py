import sys
import random
import asyncio
import zmq
import zmq.asyncio
ctx = zmq.asyncio.Context()
async def run_worker(portA=5556, portB=5557):
    sock_pull = ctx.socket(zmq.PULL)
    sock_pull.connect(f'tcp://localhost:{portA}')
    sock_push = ctx.socket(zmq.PUSH)
    sock_push.connect(f'tcp://localhost:{portB}')
    while True:
        data = await sock_pull.recv_pyobj()
        if isinstance(data, int) or isinstance(data, float):
            sys.stdout.write('*')
            sys.stdout.flush()
            await asyncio.sleep(data * 0.01)
        x = '+' if int(data) % 2 == 0 else '-'
        sys.stdout.write(f'\b{x}')
        sys.stdout.flush()
        await sock_push.send_string(x)
if __name__ == '__main__':
    asyncio.run(run_worker())