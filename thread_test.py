import threading
import time

def thread1():
    for i in range(5):
        print("thread1 +++++")
        time.sleep(0.1)

def thread2():
    for i in range(5):
        print("thread2 +++++")
        time.sleep(0.1)

th1 = threading.Thread(target=thread1)
th2 = threading.Thread(target=thread2)

th1.start()
th2.start()

th1.join()
th2.join()

print("main END!")