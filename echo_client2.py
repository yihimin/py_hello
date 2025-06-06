import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9999))

while True:
    send_data = input("입력: ") 
    sock.sendall(bytes(send_data, "utf-8"))

    recv_data = sock.recv(1024)
    decoded = recv_data.decode()
    print(f"서버 응답: {decoded}")

    if "축하합니다" in decoded:
        break

print("클라이언트 종료!")
sock.close()
