import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    users = {}  # username: (socket, address)

    def broadcast(self, msg, exclude=None):
        for username, (sock, addr) in self.users.items():
            if username != exclude:
                sock.send(msg.encode())

    def send_user_list(self):
        user_list_msg = "/users:" + ",".join(self.users.keys())
        for username, (sock, addr) in self.users.items():
            sock.send(user_list_msg.encode())


    def sendTo(self, target, msg):
        if target in self.users:
            self.users[target][0].send(msg.encode())
        else:
            self.request.send(f"⚠️ 존재하지 않는 사용자입니다: {target}\n".encode())

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send("이미 등록되어 있습니다.\n".encode())
            return None
        self.users[username] = (conn, addr)
        self.broadcast(f"📥 {username}이 입장했습니다.")
        print(f"채팅 참여 인원 {len(self.users)}")
        return username

    def delUser(self, username):
        if username in self.users:
            del self.users[username]
            self.broadcast(f"📤 {username}이 퇴장했습니다.")
            print(f"채팅 참여 인원 {len(self.users)}")

    def handle(self):
        print(f"[접속] {self.client_address[0]}")

        while True:
            self.request.send("이름을 입력하세요: ".encode())
            username = self.request.recv(1024).decode().strip()
            if self.addUser(username, self.request, self.client_address):
                break

        while True:
            data = self.request.recv(1024)
            decoded = data.decode().strip()
            if decoded.lower() == "end":
                self.request.close()
                break

            print(f"[{username}] {decoded}")

            if decoded.startswith("/w "):  # 귓속말 명령어
                try:
                    _, target, msg = decoded.split(" ", 2)
                    self.sendTo(target, f"💌 (귓속말) [{username}]: {msg}")
                    self.request.send(f"📩 (귓속말 보냄) → {target}: {msg}\n".encode())
                except ValueError:
                    self.request.send("⚠️ 사용법: /w 닉네임 메시지\n".encode())
            else:
                self.broadcast(f"[{username}]: {decoded}")

        print(f"[{username}] 접속 종료")
        self.delUser(username)

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

print("🟢 chat server start...")

chat_serv = ChatServer(("", 9999), MyHandler)
try:
    chat_serv.serve_forever()
except KeyboardInterrupt:
    print("\n서버 종료됨")
    chat_serv.shutdown()
    chat_serv.server_close()
