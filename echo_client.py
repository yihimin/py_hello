import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9999))

send_data = input("입력: ") 
sock.sendall(bytes(send_data, "utf-8"))

recv_data = sock.recv(1024)
print(f"recv: {recv_data}")

print("클라이언트 종료!")
sock.close()
