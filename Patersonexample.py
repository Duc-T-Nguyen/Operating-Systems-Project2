import threading
import time

shared_time = 0
flags = [False, False]
turn = 0


def enter(id): 
    i = 1 - id
    flags[id] = True

    global turn
    turn = i
    while flags[i] and turn == i:
        pass

def exit(id):
    flags[id] = False

def thread(id): 
    global shared_time
    for _ in range(3):
        enter(id)
        temp = shared_time
        time.sleep(.10)
        shared_time = temp + 1
        exit(id)
        time.sleep(.10)

thread0 = threading.Thread(target=thread, args=(0,))
thread1 = threading.Thread(target=thread, args=(1,))

thread0.start()
thread1.start()

thread0.join()
thread1.join()

