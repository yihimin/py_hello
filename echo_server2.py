import socket

#1.소켓 생성(ipv4 tcp)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#2.바인딩(빈 문자열은 모든 IP 인터페이스 허용, 포트 9999에서 수신)
sock.bind(("" , 9999))

#3.접속 대기 (기본 대기 큐 설정)
sock.listen()
print("The Server Start...")

#4.접속 수락(클라이언트 연결을 수락하고, 연결 소켓과 주소 반환)
conn, addr = sock.accept()

while True:
    #5.데이터 수신 (클라이언트로부터 최대 1024바이트 수신)
    read_data = conn.recv(1024)
    print("recv : {}".format(read_data.decode()))

    if read_data.decode() == "end":
        break

    #5-1. 데이터 송신
    conn.sendall(read_data)
    print("send : {}".format(read_data.decode()))

#6.접속 종료 (클라이언트 연결 종료 + 서버 소켓도 종료)
conn.close()
sock.close()