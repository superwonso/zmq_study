import zmq
def client(data_port=5556, com_port=5558):
  ctx = zmq.Context()
  # 1. SUB 소켓 연결
  sock_sub = ctx.socket(zmq.SUB)
  sock_sub.setsockopts_string(zmq.SUBSCRIBE, '9')
  sock_sub.connect(f'tcp://localhost:{data_port}')
  # 2. PULL 소켓 연결
  sock_pull = ctx.socket(zmq.PULL)
  sock_pull.connect(f'tcp://localhost:{com_port}')
  # 3. 폴러 생성 및 설정
  poller = ctx.Poller()
  poller.register(sock_sub, zmq.POLLIN)
  poller.register(sock_pull, zmq.POLLIN)
  # 폴러로부터 이벤트 수신
  should_continue = True
  while should_continue:
    # 4. 각각의 이벤트는 (소켓, 이벤트), (소켓, 이벤트) ... 의 형태로 전달
    # 이를 사전 타입으로 변환
    socks = dict(poller.poll())
    if socks.get(sock_pull, None) == zmq.POLLIN:
      command = sock_pull.recv_string()
      if command == 'EXIT':
         print('This client will be terminated...')
         should_continue = False
    if socks.get(sock_sub, None) == zmq.POLLIN:
      topic, msg = sock_sub.recv_string().split(' ', 1)
      print(f'Processing: {msg}')


      