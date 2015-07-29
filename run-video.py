#!/usr/bin/python

import paramiko
import threading
import time
import sys
from get_power2 import ServoPower

def getPower():
    global s
    s = ServoPower()
    s.start()

def dump_q(q, to_write):
    t_prev = 0.0
    e_l = 0.0
    e_b = 0.0
    target = open(to_write, 'w')
    
    while not q.empty():
        (t, l, b) = q.get()
        #print t, l, b
        e_l += (t - t_prev) * l
        e_b += (t - t_prev) * b
        #print t, (t - t_prev) * l, (t - t_prev) * b, e_l, e_b
	target.write('%f %f %f %f %f\n' % (t, (t - t_prev) * l, (t - t_prev) * b, e_l, e_b))
        t_prev  = t
        #print t, e_l, e_b

def main():
    global t, s
  
    set_governor = 'sudo sh -c \'echo ' + sys.argv[1] + '> /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor\''
    to_run = 'cd work/rt-app/doc/examples; ' +  set_governor + '; sudo taskset -c 0,1 ../workgen video-short.json'
    to_write = 'video-short-' + sys.argv[1] + '.data'
    print to_run

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    t = threading.Thread(target=getPower)

    ssh.connect('192.168.1.35', username='freedom')
    t.start()
    stdin, stdout, stderr = ssh.exec_command(to_run, get_pty=True)

    stdin.write('freedom\n')
    stdin.flush()

    data = stdout.read().splitlines()

    for line in data:
       print line

    s.stop()
    q = s.data()
    dump_q(q, to_write)
    t.join()

if __name__ == "__main__":
    main()
