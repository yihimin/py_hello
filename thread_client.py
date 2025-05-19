import socket      # 소켓 통신을 위한 모듈
import threading   # 멀티쓰레드를 위한 모듈
import time        # 일시정지를 위한 모듈

# 🔼 송신 전용 쓰레드 함수
def send_thread(sock):
    while True:
        send_data = input("입력: ")  # 사용자로부터 입력 받기
        sock.sendall(bytes(send_data, "utf-8"))  # 문자열을 바이트로 변환 후 전송

        if send_data == "end":  # "end" 입력 시 종료
            print("종료 메세지 송신함")
            break

        time.sleep(3)  # 3초 대기 (너무 빠르게 반복되지 않도록)

# 🔽 수신 전용 쓰레드 함수
def recv_thread(sock):
    while True:
        recv_data = sock.recv(1024)  # 최대 1024바이트 수신
        print(f"recv : {recv_data.decode()}")  # 수신 데이터 출력

        if recv_data.decode() == "end":  # "end" 수신 시 종료
            print("클라이언트 종료!")
            sock.close()  # 소켓 닫기
            break

# 클라이언트 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결 시도 (127.0.0.1:9999 로 접속)
sock.connect(("127.0.0.1", 9999))

# 송신 및 수신 쓰레드 생성
sth = threading.Thread(target=send_thread, args=(sock,))  # ✅ args (복수형!)로 전달
rth = threading.Thread(target=recv_thread, args=(sock,))

# 두 쓰레드 시작
sth.start()
rth.start()
