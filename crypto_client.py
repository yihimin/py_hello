import socket
import threading
from nacl.public import PrivateKey, PublicKey, Box
from datetime import datetime
import sys

class ChatClient:
    def __init__(self, server_host='127.0.0.1', server_port=9999):
        self.server_host = server_host
        self.server_port = server_port
        self.running = True
        
        print("=" * 50)
        print("💬 송신자 A - 비대칭키 채팅 클라이언트")
        print("=" * 50)
        
        # 송신자 A의 키 생성
        self.private_key = PrivateKey.generate()
        self.public_key = self.private_key.public_key
        
        print(f"🔑 송신자 A 개인키 생성: {len(self.private_key.encode())} bytes")
        print(f"🔓 송신자 A 공개키 생성: {len(self.public_key.encode())} bytes")
        print()
        
    def connect_to_server(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"🔗 서버 연결 시도: {self.server_host}:{self.server_port}")
            self.sock.connect((self.server_host, self.server_port))
            print("✅ 서버 연결 성공!")
            
            # 키 교환
            print("🔄 키 교환 시작...")
            
            # 서버 공개키 수신
            server_public_key_bytes = self.sock.recv(1024)
            server_public_key = PublicKey(server_public_key_bytes)
            print("📥 수신자 B 공개키 수신 완료")
            
            # 클라이언트 공개키 전송
            self.sock.send(self.public_key.encode())
            print("📤 송신자 A 공개키 전송 완료")
            
            # Box 생성 (송신자 A용)
            self.chat_box = Box(self.private_key, server_public_key)
            print("📦 송신자 A Box 생성 완료")
            print()
            
            # 이름 입력 및 전송
            name = input("👤 송신자 A 이름을 입력하세요: ").strip()
            if not name:
                name = "송신자 A"
            
            name_encrypted = self.chat_box.encrypt(name.encode('utf-8'))
            self.sock.send(name_encrypted)
            
            # 환영 메시지 수신
            welcome_encrypted = self.sock.recv(1024)
            welcome_msg = self.chat_box.decrypt(welcome_encrypted).decode('utf-8')
            print(f"📢 서버: {welcome_msg}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return False
    
    def receive_messages(self):
        """서버로부터 메시지 수신하는 스레드"""
        while self.running:
            try:
                encrypted_data = self.sock.recv(4096)
                if not encrypted_data:
                    break
                
                decrypted_msg = self.chat_box.decrypt(encrypted_data)
                message = decrypted_msg.decode('utf-8')
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n📨 [{timestamp}] 수신자 B로부터 응답:")
                print(f"   🔒 암호문 수신: {len(encrypted_data)} bytes")
                print(f"   🔓 복호화된 응답: '{message}'")
                print("-" * 40)
                print("💬 메시지 입력 (quit 입력 시 종료): ", end="", flush=True)
                
            except Exception as e:
                if self.running:
                    print(f"❌ 메시지 수신 오류: {e}")
                break
    
    def start_chat(self):
        if not self.connect_to_server():
            return
        
        # 메시지 수신 스레드 시작
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        print("💬 채팅 시작! 메시지를 입력하세요 (quit 입력 시 종료)")
        print("=" * 50)
        
        try:
            while self.running:
                message = input("💬 메시지 입력: ").strip()
                
                if not message:
                    continue
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # 메시지 암호화 및 전송
                encrypted_msg = self.chat_box.encrypt(message.encode('utf-8'))
                self.sock.send(encrypted_msg)
                
                print(f"📤 [{timestamp}] 송신자 A 메시지 전송:")
                print(f"   💬 원본 메시지: '{message}'")
                print(f"   🔒 암호화하여 전송: {len(encrypted_msg)} bytes")
                print(f"   🔐 암호문: {encrypted_msg[:50]}{'...' if len(encrypted_msg) > 50 else ''}")
                
                if message.lower() == 'quit':
                    print("👋 채팅을 종료합니다...")
                    break
                    
        except KeyboardInterrupt:
            print("\n⚠️ 채팅 중단")
        finally:
            self.running = False
            self.sock.close()
            print("🔚 클라이언트 종료")

if __name__ == "__main__":
    client = ChatClient()
    client.start_chat()