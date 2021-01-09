import socket


class ClientSocekt:
    def __init__(self, host: int="localhost", port: int=7474) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.BUFFER: int = 4048
        self.host = host
        self.port = port

    def start(self) -> NoReturn:
        host = self.host
        port = self.port
        sock = self.socket

        sock.connect((host, port))
        while True:
            with sock:
                try:
                    self.start_communication(sock)
                except Disconnect:
                    ...
