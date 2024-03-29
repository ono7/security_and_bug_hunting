#!/usr/bin/env python
""" find open sessions

    Fri May 29 7:44:12 PM 2020

    __author__ = 'Jose Lima'

"""
from threading import Thread, Lock
from services import get_db
import socket
import queue

port = 22

# adjust socket timeout if its too aggressive
socket.setdefaulttimeout(0.25)

# protect our threads, for printing and updating
lock = Lock()

num_threads = 15
ips_q = queue.Queue()

sql_update = """ UPDATE records SET is_alive = ?
    WHERE ip = ?
"""


# pylint: disable=W0703
def port_scan(host, port):
    """ connect or die!! """
    s = socket.socket()
    try:
        s = s.connect((host, port))
        return True
    except Exception:
        return False


c = get_db("results.db")
data = c.execute("SELECT ip FROM records;")

# fill queue
for x in data:
    ips_q.put(x[0])

# tasty threads go here
def scan(i, q, port):
    _ = i
    while True:
        # get item from queue
        ip = q.get()
        if port_scan(ip, port):
            with lock:
                print(ip, "is alive")
                alive.setdefault(ip, port)
        # update queue, this thread is done
        q.task_done()


# records our progress
alive = dict()

# start the thread pool
for i in range(num_threads):
    worker = Thread(target=scan, args=(i, ips_q, port))
    worker.setDaemon(True)
    worker.start()

# wait until worker threads are done to exit
ips_q.join()

while True:
    try:
        ips_q.get_nowait()
    except queue.Empty:
        break

# commit findings to db
for ip, stat in alive.items():
    c.execute(sql_update, (str(stat), ip))
