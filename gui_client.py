import tkinter as tk
from tkinter import ttk
import socket
from threading import Thread
import datetime

def send(event=None):
    msg = input_msg.get()
    if msg:
        try:
            sock.send(bytes(msg, "utf-8"))
        except:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, "⚠️ 서버와 연결되지 않았습니다\n")
            chat_box.config(state="disabled")
        input_msg.set("")
        if msg == "end":
            sock.close()
            win.quit()

def recvMessage():
    try:
        while True:
            msg = sock.recv(1024)
            now = datetime.datetime.now().strftime("%H:%M:%S")
            decoded = msg.decode("utf-8")

            # 시간 붙인 메시지
            formatted = f"⏰ [{now}] {decoded}\n"

            chat_box.config(state="normal")
            chat_box.insert(tk.END, formatted)
            chat_box.config(state="disabled")
            chat_box.see(tk.END)
    except:
        chat_box.config(state="normal")
        chat_box.insert(tk.END, "🚫 서버와의 연결이 종료되었습니다.\n")
        chat_box.config(state="disabled")

def on_delete(event=None):
    input_msg.set("end")
    send()

# 🎨 다크 테마 색상
BG_COLOR = "#2e2e2e"
FG_COLOR = "#ffffff"
BTN_COLOR = "#4CAF50"
ENTRY_COLOR = "#3c3f41"

# 🎛️ GUI 구성
win = tk.Tk()
win.title("🌙 희민's 귓속말 채팅기")
win.geometry("520x400")
win.configure(bg=BG_COLOR)
win.protocol("WM_DELETE_WINDOW", on_delete)

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background=BTN_COLOR, foreground="white")
style.configure("TEntry", fieldbackground=ENTRY_COLOR, foreground=FG_COLOR)

# 💬 채팅창
chat_frame = tk.Frame(win, bg=BG_COLOR)
chat_box = tk.Text(chat_frame, height=20, width=60, font=("Helvetica", 11),
                   bg=BG_COLOR, fg=FG_COLOR, wrap="word", borderwidth=0)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_box.config(state="disabled")
scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box["yscrollcommand"] = scrollbar.set
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# ✏️ 입력창 + 버튼
input_msg = tk.StringVar()
input_frame = tk.Frame(win, bg=BG_COLOR)
inputbox = ttk.Entry(input_frame, textvariable=input_msg, font=("Helvetica", 11), width=50)
inputbox.bind("<Return>", send)
inputbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

send_button = ttk.Button(input_frame, text="전송 ✉️", command=send)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)
input_frame.pack(fill=tk.X, padx=10)

# 🌐 서버 연결
IP = "localhost"
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

receive_thread = Thread(target=recvMessage)
receive_thread.start()

win.mainloop()
