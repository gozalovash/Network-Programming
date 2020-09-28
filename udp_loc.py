import socket
import argparse
from datetime import datetime

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print(f'server bind with {sock.getsockname()}')

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        server_text = data.decode('ascii')
        print(f'The client {address}, says {server_text}')
        server_text = f'this is a server, your data was {len(data)} bytes long'
        server_data = server_text.encode('ascii')
        sock.sendto(server_data, address)

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = f'THIS is the text from the client, we sent it at {datetime.now()}'
    data = text.encode('ascii')

    sock.sendto(data, ('127.0.0.1', port))
    print(f'the OS bind the client to {sock.getsockname()} socket')
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print(f'the server {address} sends us text: {text}')

def main():
    choices = {'client':client, 'server':server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)

if __name__ == '__main__':
    main()
