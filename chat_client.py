import socket
from threading import Thread

def recvData(sock):
    try:
        while True:
            data = sock.recv(1024)
            print(data.decode())
    except ConnectionAbortedError:
        print("서버로부터 연결이 강제로 종료됨")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 9999))

th = Thread(target=recvData, args=(sock,))
th.daemon = True
th.start()

while True :
    send_data = input("입력:")
    sock.send(send_data.encode())

    if send_data == "end":
        break

sock.close()
print("클라이언트 종료!")