import socket
import threading
from nacl.public import PrivateKey, PublicKey, Box
from datetime import datetime

class ChatServer:
    def __init__(self, port=9999):
        self.port = port
        self.clients = {}
        self.running = True
        
        # 서버(수신자 B)의 키 생성
        print("=" * 50)
        print("🔐 수신자 B - 비대칭키 채팅 서버")
        print("=" * 50)
        
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        
        print(f"🔑 수신자 B 개인키 생성: {len(self.private_key.encode())} bytes")
        print(f"🔓 수신자 B 공개키 생성: {len(self.public_key.encode())} bytes")
        print()
        
    def start_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', self.port))
        sock.listen(5)
        
        print(f"🟢 서버 시작 - 포트 {self.port}")
        print("👥 송신자 A 연결 대기 중...")
        print()
        
        try:
            while self.running:
                try:
                    conn, addr = sock.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(conn, addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except:
                    break
        except KeyboardInterrupt:
            print("\n🔚 서버 종료")
        finally:
            sock.close()
    
    def handle_client(self, conn, addr):
        client_name = None
        try:
            print(f"📡 새 연결: {addr}")
            
            # 1. 키 교환
            print("🔄 키 교환 시작...")
            
            # 서버 공개키 전송
            conn.send(self.public_key.encode())
            print("📤 수신자 B 공개키 전송 완료")
            
            # 클라이언트 공개키 수신
            client_public_key_bytes = conn.recv(1024)
            client_public_key = PublicKey(client_public_key_bytes)
            print("📥 송신자 A 공개키 수신 완료")
            
            # Box 생성 (수신자 B용)
            chat_box = Box(self.private_key, client_public_key)
            print("📦 수신자 B Box 생성 완료")
            print()
            
            # 2. 클라이언트 이름 수신
            name_encrypted = conn.recv(1024)
            name_decrypted = chat_box.decrypt(name_encrypted)
            client_name = name_decrypted.decode('utf-8')
            
            print(f"👤 송신자 A 이름: {client_name}")
            self.clients[client_name] = {'conn': conn, 'box': chat_box}
            
            # 환영 메시지 전송
            welcome_msg = f"환영합니다, {client_name}님! 채팅을 시작하세요."
            welcome_encrypted = chat_box.encrypt(welcome_msg.encode('utf-8'))
            conn.send(welcome_encrypted)
            
            print(f"✅ {client_name} 연결 완료")
            print("=" * 50)
            
            # 3. 메시지 수신 루프
            while True:
                encrypted_data = conn.recv(4096)
                if not encrypted_data:
                    break
                
                # 복호화
                try:
                    decrypted_msg = chat_box.decrypt(encrypted_data)
                    message = decrypted_msg.decode('utf-8')
                    
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    print(f"📨 [{timestamp}] 암호화된 메시지 수신:")
                    print(f"   🔒 암호문: {encrypted_data[:50]}{'...' if len(encrypted_data) > 50 else ''}")
                    print(f"   📏 암호문 길이: {len(encrypted_data)} bytes")
                    print(f"   🔓 복호화된 메시지: '{message}'")
                    print(f"   👤 송신자: {client_name}")
                    print("-" * 40)
                    
                    # 메시지가 'quit'이면 종료
                    if message.lower() == 'quit':
                        goodbye_msg = f"{client_name}님이 채팅방을 나갔습니다."
                        print(f"👋 {goodbye_msg}")
                        break
                    
                    # 에코 응답 (수신자 B가 답장)
                    response = f"수신자 B: '{message}' 메시지를 잘 받았습니다!"
                    response_encrypted = chat_box.encrypt(response.encode('utf-8'))
                    conn.send(response_encrypted)
                    
                    print(f"📤 [{timestamp}] 수신자 B 응답 전송:")
                    print(f"   💬 원본 메시지: '{response}'")
                    print(f"   🔒 암호화하여 전송: {len(response_encrypted)} bytes")
                    print("=" * 50)
                    
                except Exception as e:
                    print(f"❌ 복호화 실패: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ 클라이언트 처리 오류: {e}")
        finally:
            if client_name and client_name in self.clients:
                del self.clients[client_name]
            conn.close()
            print(f"🔌 {client_name or addr} 연결 종료")

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
