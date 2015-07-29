
#!/usr/bin/python

import xmlrpclib
import threading
import time
import signal, os
from Queue import Queue

class ServoPower:

    def handler(self, signum, frame):
        self.looping = False
        self.dump()

    def __init__(self):
        self.looping = True
        self.q = Queue()
        self.proxy = xmlrpclib.ServerProxy("http://localhost:9999/")

        self.little_rail = ['dvfs2_mw', 'sram15_mw']
        self.big_rail = ['dvfs1_mw', 'sram7_mw']

        #signal.signal(signal.SIGINT, self.handler)

    def start(self):
        self.time_start = time.time()

        while self.looping:
            self.little_p = 0
            for a in range(0, 1):
                for a in self.little_rail:
                    self.little_p += float(self.proxy.get(a))
                    self.little_p /= 1.0

            self.big_p = 0
            for a in range(0, 1):
                for a in self.big_rail:
                    self.big_p += float(self.proxy.get(a))
                    self.big_p /= 1.0
                    
            time_now = time.time() - self.time_start
            #print time_now, little_p, big_p
            self.q.put((time_now, self.little_p, self.big_p))

    def stop(self):
        self.looping = False
        #self.dump()

    def data(self):
        return self.q
        
    def dump(self):
        t_prev = 0.0
        e_l = 0.0
        e_b = 0.0
        while not self.q.empty():
            (t, l, b) = self.q.get()
            #print t, l, b
            e_l += (t - t_prev) * l
            e_b += (t - t_prev) * b
            print t, (t - t_prev) * l, (t - t_prev) * b, e_l, e_b
            t_prev  = t
            #print t, e_l, e_b

def getPower():
    global s
    s = ServoPower()
    s.start()

def handler(self, signum, frame):
    global s
    print "here\n"
    s.stop()

def dump_q(q):
    t_prev = 0.0
    e_l = 0.0
    e_b = 0.0
    
    while not q.empty():
        (t, l, b) = q.get()
        #print t, l, b
        e_l += (t - t_prev) * l
        e_b += (t - t_prev) * b
        print t, (t - t_prev) * l, (t - t_prev) * b, e_l, e_b
        t_prev  = t
        #print t, e_l, e_b
  
def main():
    global t, s
    signal.signal(signal.SIGINT, handler)
    t = threading.Thread(target=getPower)
    t.start()
    time.sleep(1)
    s.stop()
    q = s.data()
    dump_q(q)
    t.join()

if __name__ == "__main__":
    main()
