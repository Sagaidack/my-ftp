import socket
import typing


class ServerSocket:
    def __init__(self, host: str="localhost", port: int=7474) -> None:
        self.socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BUFFER = 4048
        self.host = host
        self.port = port
        self.msg = Massage()

    def start(self) -> None:
       host = self.host
       port = self.port
       sock = self.socket
       sock.bind((host, port))
       sock.listen()
       while True:
           with self.sock:
               client_sock, addr = self.process_client()
               self.satart_communication(client_sock)
    
    def process_clietnt(self)
        return self.sock.accept()

    def start_communication(self, cl: socket.socket) -> None:
        handel_method(self, cl)
