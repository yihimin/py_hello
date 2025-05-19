import socketserver 

class MyHandler(socketserver.BaseRequestHandler):
#유저 관리
    users = {}

    def broadcast(self, msg):
       for sock, addr in self.users.values():
           sock.send(msg.encode())

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send("이미 등록되어 있습니다.\n".encode())

        self.users[username] = (conn, addr)
        self.broadcast("{}이 참석했습니다".format(username))
        print(f"채팅 참여 인원 {len(self.users)}")

        return username
    
    def delUser(self, username):

        del self.users[username]
        self.broadcast("{}이 퇴장했습니다".format(username))
        print("채팅 참여 인원 {}".format(len(self.users)))

    def handle(self):
        print(self.client_address[0])

        while True:
            self.request.send("이름을 입력하세요".encode())
            username = self.request.recv(1024).decode()
            if self.addUser(username, self.request, self.client_address):
                break

        while True : 
            data = self.request.recv(1024)
            print("[{}] {}".format(username, data.decode()))

            if data.decode() == "end":
                self.request.close()
                break
            self.broadcast("[{}]: {}".format(username, data.decode()))

        print("[{}] 접속종료".format(username, data.decode()))
        self.delUser(username)

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

print("chat server start...")

chat_serv = ChatServer(("", 9999), MyHandler)
chat_serv.serve_forever()
chat_serv.shutdown()
chat_serv.server_close()