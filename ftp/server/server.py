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
    
    def _process_clietnt(self)
        return self.sock.accept()

    def start_communication(self, cl: socket.socket) -> None:
        handel_method(self, cl)

    def _get_req_line(self, client_sock: socket.socket) -> str:
        obj = ""
        while True:
            byte = self.client_sock.recv(1)
            char = byte.decode("UTF-8")
            if char == "\n":
                break
            obj = obj + char
        return obj
    
    def get_method(self, cl: socket.socket) -> str:
        return self._get_req_line(cl) 
    
    def get_header(self, cl: socket.socket) -> str:
        return self._het_req_line(cl) 

    def handle_method(self, cl: socket.socket) -> None:
        self.get_method(cl)
        if method == "Download":
            self.send_file()
        elif method == "Upload":
            self.receive_file()
        elif method == "Closed":
            self.closed_connect()
