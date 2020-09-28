import argparse, socket
from datetime import datetime

BUFF_SIZE = 65535

def server(port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print(f'server bind with {sock.getsockname()}')

    while True:
        data, address = sock.recvfrom(BUFF_SIZE)
        client_text = data.decode('ascii')
        print(f'server received from {address} the following {client_text}')
        server_text = f'this is your server and the data you sent was {len(data)} bytes long. P.s: I LOVE YOU!'
        server_data = server_text.encode('ascii')
        sock.sendto(server_data, address)

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = f'Hi server <3, Are you there? sent at {datetime.now()}'
    client_text = text.encode('ascii')

    sock.sendto(client_text, ('127.0.0.1',port))
    print(f'we are binded to {sock.getsockname()} socket')
    data, address = sock.recvfrom(BUFF_SIZE)
    server_text=data.decode('ascii')
    print(f'my lovely server {address} said "{server_text}"')

def main():
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='we are here to find out whether the server and client are in love..')
    parser.add_argument('role', choices=choices, help='who speaks here')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help="UDP port num")
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)

if __name__=="__main__":
    main()