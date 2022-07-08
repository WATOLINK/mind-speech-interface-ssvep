import threading, time

def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

@setInterval(1)
def function():
    print(time.time()-ti)

ti = time.time()
stop = function() # start timer, the first call is in .5 seconds
time.sleep(10.5)
stop.set() # stop the loop
print(time.time()-ti)

'''
from threading import Thread,Event
import time
class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1):
            print(time.time()-ti)
            # call a function

stopFlag = Event()
thread = MyThread(stopFlag)
global ti
ti=time.time()
thread.start()
time.sleep(10.5)
# this will stop the timer
stopFlag.set()
'''