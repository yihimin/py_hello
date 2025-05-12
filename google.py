import socket

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with socket.socket() as sock:
    sock.connect(("www.google.com", 80))
    sock.send("GET \n".encode())
    data = sock.recv(1024)
    print(data.decode())
#sock.close()