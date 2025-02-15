import socket
import random

class Server():
    def __init__(self):
        self.init_tcpIp = '0.0.0.0'
        self.init_tcpPort = 26100
        self.init_buffSize = 30

    def createSocket(self):
        print("[INFO] Creating socket...")
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("[INFO] Socket successfully created")

        return s
    
    def endSocket(self, s):
        print("[INFO] Disconnecting Socket...")
        s.close()
        print("[INFO] Socket disconnected successfully")
    
    def setupSocket(self, s, tcpIp, tcpPort):
        s.bind((tcpIp,tcpPort))
        print("[INFO] Socket is binded to port",tcpPort)

    def sendToClient(self, c, msg, buffSize, isSend=True):
        print("[INFO] Encoding data...")
        e_msg = msg.encode('utf-8')

        print(f"[INFO] Sending data to client... {msg}")
        c.send(e_msg)

        if isSend:
            self.verifySendToClient(c, msg, buffSize)

    def verifySendToClient(self, c, msg, buffSize):
        print("[INFO] Verifying data send to client")
        data = self.reciveFromClient(c, buffSize, False)
        if data != msg:
            print("[ERROR] Data recived from client did not match data send")
            raise IOError
        else:
            print("[INFO] Data sent successfully to client")

    def reciveFromClient(self, c, buffSize, isRecive=True):
        print("[INFO] Receiving data from client...")
        data = c.recv(buffSize)

        print("[INFO] Decoding received data...")
        data = data.decode('utf-8')

        print("[INFO] Received data from client : ",data)

        if isRecive:
            self.sendToClient(c, data, buffSize, False)

        return data

    def handshakeClients(self):
        playerCounter = 1
        playerLimit = 10
        players = []

        s = self.createSocket()
        self.setupSocket(s, self.init_tcpIp, self.init_tcpPort)

        s.listen(1)
        print("[INFO] Socket is listening")

        while playerCounter<=playerLimit:
            c,addr = s.accept()
            print("[INFO] Connection address from",addr)

            msg = f"{self.init_tcpPort+playerCounter}"
            self.sendToClient(c, msg, self.init_buffSize)

            if playerCounter == 1:
                data = self.reciveFromClient(c, self.init_buffSize)

                self.numPlayers = int(data)
                playerLimit = self.numPlayers

            players.append((addr[0], self.init_tcpPort+playerCounter))

            print("[INFO] Disconnecting Client connection...")
            c.close()

            playerCounter += 1

        self.endSocket(s)
        self.players = players

    def game(self):
        self.deck = self.generateDeck()
        self.sendPlayerHand()

    def generateDeck(self):
        deck=[]
        for suit in ["spades", "clubs", "hearts", "diamonds"]:
            suitList = list(range(2,11))
            suitList.extend(["jack", "queen", "king", "ace"])
            for card in suitList:
                deck.append(suit+str(card))

        random.shuffle(deck)
        return deck
    
    def sendPlayerHand(self):
        for player in self.players:
            tcpIp = player[0]
            tcpPort = player[1]
            buffSize = 30

            s = self.createSocket()

            print("[INFO] Connecting Socket to port",tcpPort)
            s.connect((tcpIp, tcpPort))
            print("[INFO] Socket connected successfully to port", tcpPort)

            for i in range(7):
                msg = self.deck[0]
                self.deck.pop(0)
                self.sendToClient(s, msg, buffSize)

    def run(self):
        self.handshakeClients()
        self.game()

if __name__ == "__main__":
    server = Server()
    server.run()