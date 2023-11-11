import socket
from threading import Thread

from DNSGenerator import DNSGenerator

server_ip = '127.0.0.1'
port = 5353


class ClientHandler(Thread):

    def __init__(self, client_address, input_data, dns_server: socket):
        super().__init__()
        self.client_address = client_address
        self.input_data = input_data
        self.dns_server = dns_server

    def response_client(self):
        dns_generator = DNSGenerator(data=self.input_data)
        response = dns_generator.run()
        self.dns_server.sendto(response, self.client_address)
        print(f'Record for {dns_generator.domain} sent to {self.client_address}')


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((server_ip, port))
    print(f'DNS server is listening on {server_ip}:{port}...')
    while True:
        data, address = server.recvfrom(650)
        ClientHandler(client_address=address, input_data=data, dns_server=server).response_client()


if __name__ == '__main__':
    main()
