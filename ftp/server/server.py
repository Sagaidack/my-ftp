import socket
import typing
from typing import Tuple, NoReturn
import io

from ftp.server.massage import Massage
from .status_code import StatusCode
from .exception import Disconnect


class ServerSocket:
    def __init__(self, host: str="localhost", port: int=7474) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BUFFER: int = 4048
        self.host = host
        self.port = port
        self.code_msg = StatusCode()
        self.msg = Massage()

    def start(self) -> NoReturn:
        host = self.host
        port = self.port
        sock = self.socket

        sock.bind((host, port))
        sock.listen()
        while True:
            with sock:
                client_sock, addr = self._process_client(sock)
                try:
                    self.start_communication(client_sock)
                except Disconnect:
                    ...
            
    
    def _process_client(self, sock) -> typing.Tuple:
        return sock.accept()

    def start_communication(self, cl: socket.socket) -> None:
        self.handle_method(cl)

    def _get_req_line(self, client_sock: socket.socket) -> bytes:
        byte_line: bytes
        while True:
            byte = client_sock.recv(1)
            if byte == b"\n":
                break
            byte_line = byte_line + byte
        return byte_line
    
    def get_method(self, cl: socket.socket) -> bytes:
        return self._get_req_line(cl) 
    
    def get_header(self, cl: socket.socket) -> bytes:
        return self._get_req_line(cl) 

    def handle_method(self, cl: socket.socket) -> None:
        method = self.get_method(cl)
        if method == "Download":
            self.send_file(cl)
        elif method == "Upload":
            self.receive_file(cl)
        elif method == "Closed":
            self.closed_connect(cl)

    def receive_file(self, cl: socket.socket) -> None:
        buffer = self.BUFFER

        header = self.get_header(cl)
        with open(header, "wb") as file:
            bdata = self.write_to_file(file, cl, buffer)
            self.send_respones(bdata, cl) 

    def _rec_data(self, cl: socket.socket, buffer: int) -> bytes:
        return cl.recv(buffer)

    def write_to_file(self, file, cl: socket.socket, buffer) -> bytes:
        bdata = self._rec_data(cl, buffer)
        file.write(bdata)
        return bdata

    def closed_connect(self, client) -> NoReturn:
        client.close()
        client = None
        raise Disconnect
        

    def send_file(self, cl: socket.socket) -> None:
        buffer = self.BUFFER
        read_file = self._read_file

        header = self.get_header(cl)
        with open(header, "rb") as file:
            while True:
                bdata: bytes = read_file(file, buffer)
                self.send_respones(bdata, cl)
                self._receive_req(cl, buffer)
     
    def _receive_req(self, cl: socket.socket, buffer: int) -> Tuple[bytes, bytes, bytes]:
        status = self._get_req_line(cl)
        message = self._get_req_line(cl)
        data_bytes = cl.recv(2048)
        return status, message, data_bytes 

    def _read_file(self, file: io.BufferedReader, buffer: int) -> bytes:
        return file.read(buffer)
            
    def send_respones(self, bdata: bytes, cl: socket.socket) -> None:
        respon: bytes = self.create_respones(bdata)
        cl.send(respon)

    def create_respones(self, bdata: bytes) -> bytes:
        msg = self.msg
        code_msg = self.code_msg

        if bdata == b"":
            status_code: str = msg.process_is_over
            massage: str = msg.process_is_over
        respon: bytes = (status_code + "\n" + massage + "\n").encode("UTF-8")
        if bdata != b"":
            status_code = msg.process_is_not_over
            massage = code_msg.process_is_not_over
            respon = (status_code + "\n" + massage + "\n").encode("UTF-8")
        return respon
