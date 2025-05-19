import socket      # 소켓 통신을 위한 모듈
import threading   # 멀티 쓰레드를 위한 모듈

# 클라이언트로부터 메시지를 받고 에코(그대로 다시 보내기) 처리하는 함수
def thread_recv(client_socket, addr):
    while True:
        recv_data = client_socket.recv(1024)   # 클라이언트로부터 최대 1024바이트 수신
        print(f"{addr}에서 보낸 메세지 : {recv_data.decode()}")  # 수신한 메시지 출력

        client_socket.sendall(recv_data)       # 받은 메시지를 그대로 다시 전송 (에코)

        if recv_data.decode() == "end":        # "end"라는 메시지가 오면 종료
            print(f"{addr}이 종료를 원합니다.")
            client_socket.close()              # 소켓 연결 종료
            break

# TCP/IP 소켓 생성 (IPv4 + TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓에 주소 지정 (빈 문자열 ""은 모든 인터페이스에서의 접속 허용)
sock.bind(("", 9999))

# 최대 연결 대기 수 설정
sock.listen()
print("The server start.....")

# 클라이언트 접속 수락 (소켓 객체와 주소 반환)
conn, addr = sock.accept()  # ✅ 괄호 꼭 필요!

# 수신 전용 스레드 생성 및 실행
recv_handler = threading.Thread(target=thread_recv, args=(conn, addr))  # ✅ 튜플로 전달!
recv_handler.start()
