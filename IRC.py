import socket
import sys
import threading


# -------------------- #
#   GLOBAL VARIABLES
# -------------------- #

userDict = {}
port = 8080
host = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lock = threading.Lock()
# Reuse the same port without waiting for the OS
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.bind((host, port))
except socket.error:
    print("Socket bind error")
    sys.exit()


# -------------------- #
# Function declarations
# -------------------- #

def sendData(data):
    print(sock)
    sock.send(data)


def userAppend(connID, nick):
    userDict[nick] = connID


def printDict():
    for i in userDict.keys():
        print(i, userDict[i])


def userDel(connID):
    del userDict[connID]


def sendAll(nick, message):
    for key in userDict.keys():
        if key == nick:
            continue
        else:
            userDict[key].send(message.encode("utf-8"))


# ------------------------- #
#      Client class
# ------------------------- #


class connection(threading.Thread):

    def __init__(self, conn, addr, lock):
        threading.Thread.__init__(self)
        self.conn = conn
        self.dict = {}
        self.addr = addr
        self.lock = lock
        self.nick = None
        self.user = None

    def run(self):
        print("new Thread")
        while(True):
            data = self.conn.recv(2048).decode('utf-8')

            if data.rstrip(" ") == "":
                continue

            if data.rstrip('\r\n') == ":quit":
                self.clean()
                break

            if len(data.split()) == 4:
                if data.split()[0] == ":USER" and data.split()[2] == ":NICK":
                    self.user = data.split()[1].rstrip('\r\n')
                    self.nick = data.split()[3].rstrip('\r\n')
                    message = "{} has joined the room\n".format(self.nick)
                    sendAll(self.nick, message)
                    self.lock.acquire()
                    try:
                        userAppend(self.conn, self.nick)
                    finally:
                        self.lock.release()

            if (not self.nick or not self.user):
                message = "Enter username and nick please\nUSAGE ->"\
                          ":USER <username> :NICK <nickname> \n"
                self.dataSend(message)
                continue

            if data.split()[0] == ":USER":
                self.user = data.split()[1].rstrip('\r\n')

            if data.split()[0] == ":SENDALL":
                self.lock.acquire()
                try:
                    sendAll(self.nick)
                finally:
                    self.lock.release()

            print(data.rstrip('\r\n'))

    def dataSend(self, data):
        self.conn.send(data.encode("utf-8"))

    def clean(self):
        print("Quitting")
        self.conn.close()


while(True):
    try:
        sock.listen(10)
        conn, addr = sock.accept()
        child = connection(conn, addr, lock)
        child.start()
    except KeyboardInterrupt:
        sock.close()
