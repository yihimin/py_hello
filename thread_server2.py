import socket     
import threading   

numClient = 0  #접속 클라이언트 카운트 변수

def thread_recv(client_socket, addr):
    global numClient #전역 변수 사용을 위한 선언

    while True:
        recv_data = client_socket.recv(1024)  
        #각 스레드별 메세지 출력
        print(f"Thread Name {threading.current_thread().name}에서 보낸 메세지 : {recv_data.decode()}")  

        if recv_data.decode() == "end":
            numClient = numClient - 1 #접속자 수 감소        
            print(f"{addr}이 종료를 원합니다.")
            print(f"현재 서버에 접속된 클라이언트 수 {numClient}")
            client_socket.close()              
            break

        client_socket.sendall(recv_data) #데이터 송신 에코

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("", 9999))

sock.listen()
print("The server start.....")

#멀티스레드 통신
while True:
    # 클라이언트 접속 수락 (소켓 객체와 주소 반환)
    conn, addr = sock.accept()  

    numClient = numClient + 1
    print(f"현재 {addr}이 접속했습니다.")
    print(f"현재 서버에 접속된 클라이언트 수 {numClient}")

    # 수신 전용 스레드 생성 및 실행
    recv_handler = threading.Thread(target=thread_recv, args=(conn, addr), name=addr)  # ✅ 튜플로 전달!
    recv_handler.start()
