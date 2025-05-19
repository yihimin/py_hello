import socketserver  # socket + thread + 처리기능을 포함한 서버 프레임워크

# ➊ 요청이 올 때마다 호출될 Handler 클래스 정의
class MyHandler(socketserver.BaseRequestHandler):
    def handle(self): #오버라이딩
        # ➋ 클라이언트가 보낸 데이터 수신
        self.data = self.request.recv(1024)
        print("데이터 수신: {}".format(self.data.decode()))
        
        # ➌ 받은 데이터를 그대로 다시 전송 (에코)
        self.request.sendall(self.data)

# ➍ 서버 실행
print("chat server start...")

# TCPServer 객체 생성 (포트 9999에서 대기)
sock = socketserver.TCPServer(("", 9999), MyHandler)

# 클라이언트 요청을 무한히 처리
sock.serve_forever()
