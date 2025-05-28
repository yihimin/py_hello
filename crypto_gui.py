import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
from nacl.public import PrivateKey, PublicKey, Box

# 키 생성
client_sk = PrivateKey.generate()
client_pk = client_sk.public_key

HOST = '127.0.0.1'
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except Exception as e:
    raise SystemExit(f"서버에 연결할 수 없습니다: {e}")

# 서버 공개키 수신
server_pk_bytes = sock.recv(1024)
server_pk = PublicKey(server_pk_bytes)

# 클라이언트 공개키 전송
sock.send(client_pk.encode())

# Box 생성
client_box = Box(client_sk, server_pk)

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 암호화 채팅 - 송신자 A")

        self.chat_log = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20)
        self.chat_log.pack(padx=10, pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(padx=10, pady=5, side=tk.LEFT)
        self.entry.bind('<Return>', self.send_message)

        self.send_button = tk.Button(root, text="전송", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.LEFT)

        self.name = simpledialog.askstring("이름 입력", "사용자 이름을 입력하세요:", parent=root)
        if not self.name:
            self.name = "송신자 A"

        sock.send(client_box.encrypt(self.name.encode()))
        welcome_encrypted = sock.recv(1024)
        welcome_msg = client_box.decrypt(welcome_encrypted).decode('utf-8')
        self.write_message(f"[서버] {welcome_msg}")

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def write_message(self, message):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, message + '\n')
        self.chat_log.config(state='disabled')
        self.chat_log.yview(tk.END)

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            encrypted = client_box.encrypt(msg.encode())
            sock.send(encrypted)
            self.write_message(f"[나] {msg}")
            self.entry.delete(0, tk.END)
            if msg.lower() == 'quit':
                self.root.quit()

    def receive_messages(self):
        while True:
            try:
                encrypted = sock.recv(4096)
                if not encrypted:
                    break
                decrypted = client_box.decrypt(encrypted).decode('utf-8')
                self.write_message(f"[수신자 B] {decrypted}")
            except Exception as e:
                self.write_message(f"[오류] 수신 실패: {e}")
                break

root = tk.Tk()
gui = ChatGUI(root)
root.mainloop()
