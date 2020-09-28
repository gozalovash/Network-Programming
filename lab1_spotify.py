import socket, argparse, random
from datetime import datetime

BUFF_SIZE = 65535

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.address, self.port))
        print(f'Listening at {sock.getsockname()}')

        while True:
            data, address = sock.recvfrom(BUFF_SIZE)

            if random.random() < 0.7:
                print(f'server has dropped the package from {address}')
                continue

            text=data.decode('ascii')
            print(f'client at address {address} said "{text}"')
            server_says = f'this is a server, from Slytherine, and your data was {len(data)} bytes long'
            server_data = server_says.encode('ascii')
            sock.sendto(server_data, address)


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def backoff(self, interval):
        backoff = {1 : 2, 2 : 4, 3 : 1}
        return backoff[interval]


    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.address, self.port))
        print(f'Client socketname is {sock.getsockname()}')
        client_text = f' I am a client, and I am from Griffindor! I decided it now, at {datetime.now()}'

        delay = 0.1
        while True:
            sock.send(client_text.encode('ascii'))
            print(f'waiting for {delay} sec')
            sock.settimeout(delay)
            try:
                data = sock.recv(BUFF_SIZE)
            except socket.timeout as exc:
                delay *= (2 if self.interval() == 2 else 3)
                if delay > self.backoff(self.interval()):
                    raise RuntimeError('The message is not received, something is wrong.') from exc
            else:
                break
        print(f"server received: {data.decode('ascii')}")

    def todayAt(self, hr, min=0, sec=0, micros=0):
        now = datetime.now().time()
        return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)

    def interval(self):
        time = datetime.now().time()
        if self.todayAt(12) < time < self.todayAt(17):
            return 1
        elif self.todayAt(17) < time < self.todayAt(23, 59, 59):
            return 2
        else:
            return 3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=['client', 'server'])
    parser.add_argument('-H', metavar='HOST', default='127.0.0.1')
    parser.add_argument('-p', metavar='PORT', type=int, default=1025)

    args = parser.parse_args()
    if args.role == 'server':
        running = Server(args.H, args.p).bind()
    else:
        running = Client(args.H, args.p).connect()

if __name__ == "__main__":
    main()









