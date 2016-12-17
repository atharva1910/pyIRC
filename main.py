import socket
import sys


class connection:

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.recv()

    def send(self):
        message = "hello, Welcome"
        conn.send(message.encode('utf-8'))

    def recv(self):
        while(True):
            data = self.conn.recv(2048).decode('utf-8')
            if data.rstrip('\r\n') == "quit":
                break
            print(data)


if __name__ == "__main__":
    port = 8080
    host = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
    except socket.error:
        print("Socket bind error")
        sys.exit()
    sock.listen(1000)
    conn, addr = sock.accept()
    # list of dictornaries??
    child = connection(conn, addr)
