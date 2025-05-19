import tkinter as tk
from tkinter import ttk
import socket
from threading import Thread
import datetime

# 사용자 색상
user_colors = {}
color_palette = ["#FF6B6B", "#6BCB77", "#4D96FF", "#FFC75F", "#A66DD4", "#FF9671"]
color_index = 0
current_username = None

def assign_color(username):
    global color_index
    if username not in user_colors:
        user_colors[username] = color_palette[color_index % len(color_palette)]
        color_index += 1
    return user_colors[username]

def send(event=None):
    target = user_select.get()
    msg = input_msg.get()
    if msg:
        try:
            if target != "전체":
                sock.send(f"/w {target} {msg}".encode("utf-8"))
            else:
                sock.send(msg.encode("utf-8"))
        except:
            chat_box.config(state="normal")
            chat_box.insert(tk.END, "⚠️ 서버와 연결되지 않았습니다\n", "system")
            chat_box.config(state="disabled")
        input_msg.set("")
        if msg == "end":
            sock.close()
            win.quit()

def recvMessage():
    while True:
        try:
            msg = sock.recv(1024)
            now = datetime.datetime.now().strftime("%H:%M:%S")
            decoded = msg.decode("utf-8").strip()

            # 유저 목록 갱신 처리
            if decoded.startswith("/users:"):
                update_user_list(decoded.replace("/users:", "").split(","))
                continue

            chat_box.config(state="normal")
            chat_box.insert(tk.END, f"[{now}] ")

            if decoded.startswith("[") and "]" in decoded:
                end = decoded.index("]")
                username = decoded[1:end]
                text = decoded + "\n"
                color = assign_color(username)
                tag = f"user_{username}"

                if username == current_username:
                    tag += "_self"
                    chat_box.tag_config(tag, foreground=color, justify="right", background="#FFE6F0")
                elif "귓속말" in decoded:
                    chat_box.tag_config(tag, foreground=color, background="#FFF5E1")
                else:
                    chat_box.tag_config(tag, foreground=color)

                chat_box.insert(tk.END, text, tag)
            else:
                chat_box.insert(tk.END, decoded + "\n", "system")

            chat_box.config(state="disabled")
            chat_box.see(tk.END)
        except:
            break

def update_user_list(users):
    user_select['values'] = ["전체"] + [u for u in users if u != current_username]
    if user_select.get() not in user_select['values']:
        user_select.set("전체")

def on_delete(event=None):
    input_msg.set("end")
    send()

# 🎨 핑크 테마
BG_COLOR = "#FFE4EC"
FG_COLOR = "#4A4A4A"
BTN_COLOR = "#FF85A2"
ENTRY_COLOR = "#FFFFFF"

win = tk.Tk()
win.title("💖 희민's 핑크 채팅기")
win.geometry("600x500")
win.configure(bg=BG_COLOR)
win.protocol("WM_DELETE_WINDOW", on_delete)

# 스타일 설정
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background=BTN_COLOR, foreground="white")
style.configure("TEntry", fieldbackground=ENTRY_COLOR, foreground=FG_COLOR)

# 채팅창
chat_frame = tk.Frame(win, bg=BG_COLOR)
chat_box = tk.Text(chat_frame, height=20, width=60, font=("Helvetica", 11),
                   bg=ENTRY_COLOR, fg=FG_COLOR, wrap="word", borderwidth=0)
chat_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_box.config(state="disabled")
chat_box.tag_config("system", foreground="#6666cc")

scrollbar = tk.Scrollbar(chat_frame, command=chat_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_box["yscrollcommand"] = scrollbar.set
chat_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# 유저 선택 드롭다운
select_frame = tk.Frame(win, bg=BG_COLOR)
user_select = ttk.Combobox(select_frame, state="readonly", width=20)
user_select.set("전체")
user_select.pack(side=tk.RIGHT, padx=10)
select_frame.pack(fill=tk.X, padx=10)

# 입력창 및 전송 버튼
input_msg = tk.StringVar()
input_frame = tk.Frame(win, bg=BG_COLOR)
inputbox = ttk.Entry(input_frame, textvariable=input_msg, font=("Helvetica", 11))
inputbox.bind("<Return>", send)
inputbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

send_button = ttk.Button(input_frame, text="전송 ✉️", command=send)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)
input_frame.pack(fill=tk.X, padx=10)

# 서버 연결
IP = "localhost"
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

# 사용자 이름 등록
username = input("이름을 입력하세요: ").strip()
sock.send(username.encode("utf-8"))
current_username = username

# 메시지 수신 스레드 시작
receive_thread = Thread(target=recvMessage)
receive_thread.start()

win.mainloop()
