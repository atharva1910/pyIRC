import socket
import sys
import main as client


def sendData(data):
    print(sock)
    sock.send(data)


def userAppend(connID, nick):
    updateAll(connID, nick)
    userDict[connID] = nick


def userDel(self, connID):
    del self.userDict[connID]


def updateAll(self, connID, nick):
    """
        Send the new connID and nick to all the users
        """
    message = "UPDATE: "+str(connID) + " " + str(nick)
    for key in self.userDict.items():
        self.sock.send(key, message.encode("utf-8"))


def delAll(self, connID, nick):
    message = "DELETE: " + str(connID)
    for key in self.userDict.items():
        self.sock.send(key, message.encode("utf-8"))


if __name__ == "__main__":
    userDict = {}
    port = 8080
    host = ""
    userDict = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
    except socket.error:
        print("Socket bind error")
        sys.exit()
    sock.listen(1000)
    conn, addr = sock.accept()
    child = client.connection(conn, addr)
    sock.close()
