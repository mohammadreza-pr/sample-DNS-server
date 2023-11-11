import socket
from socket import socket
from threading import Thread

server_ip = '127.0.0.1'
port = 5354


class ClientHandler(Thread):

    def __init__(self, client_address, input_data, dns_server: socket):
        super().__init__()
        self.client_address = client_address
        self.input_data = input_data
        self.dns_server = dns_server

    def response_client(self):
        self.dns_server.sendto(b'', self.client_address)


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, port))
    print(f'DNS server is listening on {server_ip}:{port}...')
    while True:
        data, address = server.recvfrom(650)
        ClientHandler(client_address=address, input_data=data, dns_server=server).response_client()
        print(data, address)


if __name__ == '__main__':
    main()
