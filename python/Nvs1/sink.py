import sys
import asyncio
import zmq
import zmq.asyncio
ctx = zmq.asyncio.Context()
async def run_sink(port=5557):
    sock = ctx.socket(zmq.PULL)
    sock.bind(f'tcp://*:{port}')
    # WAIT
    amount = int.from_bytes((await sock.recv()), 'big')
    for _ in range(amount):
        result = await sock.recv_string()
        sys.stdout.write(result)
        sys.stdout.flush()
if __name__ == '__main__':
    asyncio.run(run_sink())


    