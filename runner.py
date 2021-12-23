from datetime import datetime
import random
import threading
import time
import keyboard


__is_running = False

__actionner = ['&', 'é', '"', 'a', 'e', 'f']


class AntiAfkThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        anti_afk(self.delay)


def set_is_running(action: bool):
    global __is_running
    __is_running = action


def get_is_running():
    return __is_running


def __create_anti_afk_thread():
    return go("anti_afk", __set_delay())


def __get_afk_thread(thread_name):
    for t in threading.enumerate():
        if t.name == thread_name:
            return t


def __set_delay():
    return random.choice(range(30, 900))


def __start(anti_afk_thread: threading.Thread):
    print("started at " + datetime.now().strftime("%H:%M:%S"))
    time.sleep(1)
    anti_afk_thread.start()


def __stop(anti_afk_thread: threading.Thread):
    if anti_afk_thread is not None:
        print("stopped at " + datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)
        set_is_running(False)
        anti_afk_thread.join()


def go(t_name, delay):
    return AntiAfkThread(t_name, delay)


def select_actionner():
    return random.choice(__actionner)


def anti_afk(delay):
    set_is_running(True)
    keyboard.press_and_release(select_actionner())
    print("waiting " + str(delay))
    for i in range(delay):
        time.sleep(1)
        if not get_is_running():
            break


def stop_application():
    if keyboard.is_pressed('esc'):
        return True
    else:
        return False


while True:
    if keyboard.is_pressed('$') and not get_is_running():
        __start(__create_anti_afk_thread())
        time.sleep(1)
    if keyboard.is_pressed('$') and get_is_running():
        __stop(__get_afk_thread("anti_afk"))
        time.sleep(1)
    if stop_application():
        __stop(__get_afk_thread("anti_afk"))
        print("exit application")
        break
