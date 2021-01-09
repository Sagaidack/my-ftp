import socket
from typing import NoReturn

from .exception import Disconnect


class ClientSocekt:
    def __init__(self, host: str="localhost", port: int=7474) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BUFFER: int = 4048
        self.host = host
        self.port = port

    def start(self) -> None:
        host = self.host
        port = self.port
        sock = self.socket

        sock.connect((host, port))
        while True:
            with sock:
                try:
                    self.start_communication(sock)
                except Disconnect:
                    break
    
    def start_communication(self, sock: socket.socket) -> None:
        self.handle_method(sock)

    def handle_method(self, sock: socket.socket) -> None:
        method, file_path = self.create_request_init()
        if method == "Download":
            self.receive_file(sock, file_path, method)
        elif method == "Upload":
            self.send_file(sock)
        elif method == "Closed":
            self.closed_connect(sock)
    
    def create_request_init(self):
        method: str=input("enter the method: ")
        header: str=input("enter the path: ")
        return method, header

    def get_file_name(self, file_path: str):
        list_file_path_el = file_path.split("\\")
        file_name = list_file_path_el[-1]
        return file_name

    def receive_file(self, sock: socket.socket, file_path: str, method: str) -> None:
        buffer = self.BUFFER

        file_name = self.get_file_name(file_path)
        with open(file_name, "wb") as file:
            bdata = self.write_to_file(file, sock, buffer)
            self.send_req(bdata, sock, method, file_name)
    
    def send_req(self, bdata, sock, method: str, file_name: str):
        breq = self.create_request(method, file_name)
        sock.send(breq)

    def create_request(self, method: str, file_name: str):
        return method + "\n" + file_name + "\n"

    def _rec_data(self, sock: socket.socket, buffer: int) -> bytes:
        return sock.recv(buffer)

    def write_to_file(self, file, sock: socket.socket, buffer) -> bytes:
        bdata = self._rec_data(sock, buffer)
        file.write(bdata)
        return bdata

    def closed_connect(self, sock) -> NoReturn:
        sock.close()
        sock = None
        raise Disconnect

    def send_file(self, sock: socket.socket) -> None:
        ...
