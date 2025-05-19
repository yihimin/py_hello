import socketserver  # 파이썬 내장 소켓 서버 프레임워크

# 📡 클라이언트 요청을 처리하는 핸들러 클래스 정의
class MyHandler(socketserver.BaseRequestHandler):
    # 유저 목록을 저장하는 딕셔너리 (username: (socket, address))
    users = {}

    # 📢 모든 유저에게 메시지를 보내는 브로드캐스트 함수
    def broadcast(self, msg):
        for sock, addr in self.users.values():
            sock.send(msg.encode())  # 문자열을 바이트로 인코딩 후 전송

    # 🙋 유저 등록 함수
    def addUser(self, username, conn, addr):
        # 이미 존재하는 유저명일 경우 알림
        if username in self.users:
            conn.send("이미 등록되어 있습니다.\n".encode())
            return None  # 중복 시 None 반환해서 등록 실패로 처리

        # 유저 등록
        self.users[username] = (conn, addr)
        self.broadcast("{}이 참석했습니다".format(username))  # 전체에 입장 알림
        print(f"채팅 참여 인원 {len(self.users)}")

        return username  # 성공 시 username 반환

    # 🧹 유저 삭제 함수
    def delUser(self, username):
        del self.users[username]  # 유저 목록에서 제거
        self.broadcast("{}이 퇴장했습니다".format(username))  # 전체에 퇴장 알림
        print("채팅 참여 인원 {}".format(len(self.users)))

    # 🧠 클라이언트가 접속하면 자동으로 호출되는 핵심 함수
    def handle(self):
        print(self.client_address[0])  # 접속한 IP 주소 출력

        # 1️⃣ 유저명 입력 루프
        while True:
            self.request.send("이름을 입력하세요".encode())
            username = self.request.recv(1024).decode().strip()
            if self.addUser(username, self.request, self.client_address):
                break  # 등록 성공 시 루프 탈출

        # 2️⃣ 메시지 송수신 루프
        while True:
            data = self.request.recv(1024)
            decoded = data.decode().strip()
            print("[{}] {}".format(username, decoded))  # 서버 콘솔 출력

            # "end" 입력 시 종료 처리
            if decoded == "end":
                self.request.close()  # 클라이언트 소켓 닫기
                break

            # 받은 메시지를 전체 유저에게 브로드캐스트
            self.broadcast("[{}]: {}".format(username, decoded))

        # 3️⃣ 종료 후 정리 작업
        print("[{}] 접속종료".format(username))
        self.delUser(username)  # 유저 목록에서 제거

# 🧱 서버 클래스: 멀티스레딩 기능 추가한 TCP 서버 상속 정의
class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass  # 추가 설정 없음

# 🔧 서버 시작
print("chat server start...")

# 서버 인스턴스 생성 및 실행
chat_serv = ChatServer(("", 9999), MyHandler)
chat_serv.serve_forever()  # 무한 루프로 클라이언트 요청 처리

# 🔚 서버 종료 시 (KeyboardInterrupt 등)
chat_serv.shutdown()
chat_serv.server_close()