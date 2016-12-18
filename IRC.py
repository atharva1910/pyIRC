import socket
import sys
import threading


# -------------------- #
#   GLOBAL VARIABLES
# -------------------- #

userDict = {}
threads = []
port = 8080
host = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    print("Updating Dictionary")
    userDict[nick] = connID


def printDict():
    for i in userDict.keys():
        print(i, userDict[i])


def userDel(connID):
    del userDict[connID]


def updateAll():
    """
        Send the new connID and nick to all the users
    """
    message = "HEllO"
    for key in userDict.values():
        key.send(message.encode("utf-8"))


def delAll(self, connID, nick):
    message = "DELETE: " + str(connID)
    for key in self.userDict.items():
        self.sock.send(key, message.encode("utf-8"))

# ------------------------- #
#      Client class
# ------------------------- #


class connection(threading.Thread):

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.dict = {}
        self.addr = addr
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

            if len(data.split()) == 4 and data.split()[0] == ":USER":
                self.user = data.split()[1].rstrip('\r\n')
                if data.split()[2] == ":NICK":
                    self.nick = data.split()[3].rstrip('\r\n')
                userAppend(self.conn, self.nick)
                message = "{} has joined the room\n".format(self.nick)
                self.dataSend(message)

            if (not self.nick or not self.user):
                message = "Enter username and nick please\nUSAGE ->"\
                          ":USER <username> :NICK <nickname> \n"
                self.dataSend(message)
                continue

            if data.split()[0] == ":USER":
                self.user = data.split()[1].rstrip('\r\n')

            if data.split()[0] == ":SENDALL":
                updateAll()

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
        child = connection(conn, addr)
        child.start()
        threads.append(child)
    except KeyboardInterrupt:
        sock.close()
