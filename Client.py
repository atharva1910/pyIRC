class connection:

    def __init__(self, conn, addr):
        self.conn = conn
        self.dict = {}
        self.addr = addr
        self.nick = None
        self.user = None
        self.recv()
        self.conn.close()

    def recv(self):
        while(True):
            data = self.conn.recv(2048).decode('utf-8')

            if data.rstrip(" ") == "":
                continue

            if data.rstrip('\r\n') == ":quit":
                print("Quitting")
                break

            if len(data.split()) == 4 and data.split()[0] == ":USER":
                self.user = data.split()[1].rstrip('\r\n')
                if data.split()[2] == ":NICK":
                    self.nick = data.split()[3].rstrip('\r\n')
                message = "{} has joined the room\n".format(self.nick)
                self.dataSend(message)

            if (not self.nick or not self.user):
                message = "Enter username and nick please\nUSAGE ->"\
                          ":USER <username> :NICK <nickname> \n"
                self.dataSend(message)
                continue

            if data.split()[0] == ":USER":
                self.user = data.split()[1].rstrip('\r\n')

            print(data.rstrip('\r\n'))

    def dataSend(self, data):
        self.conn.send(data.encode("utf-8"))
