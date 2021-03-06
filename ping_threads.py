#!/usr/bin/env python
"""

    ping using standard linux ping to avoid being root etc etc etc...

    Tue Dec 22 10:17:16 AM 2018 CST

"""

from threading import Thread
import subprocess

try:
    import queue
except ImportError:
    import Queue as queue
import re

num_threads = 15
ips_q = queue.Queue()
out_q = queue.Queue()

ips = []
for i in range(1, 200):
    ips.append("192.168.0." + str(i))

def thread_pinger(i, q):
    """Pings hosts in queue"""
    _ = i
    while True:
        ip = q.get()
        args = ["/bin/ping", "-c", "1", "-W", "1", str(ip)]
        p_ping = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        p_ping_out = str(p_ping.communicate()[0])

        if p_ping.wait() == 0:
            # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
            search = re.search(
                r"rtt min/avg/max/mdev = (\S+)/(\S+)/(\S+)/(\S+) ms",
                p_ping_out,
                re.M | re.I,
            )
            ping_rtt = search.group(2)
            out_q.put("OK " + str(ip) + " rtt= " + ping_rtt)

        q.task_done()


for i in range(num_threads):
    worker = Thread(target=thread_pinger, args=(i, ips_q))
    worker.setDaemon(True)
    worker.start()

for ip in ips:
    ips_q.put(ip)

ips_q.join()

while True:
    try:
        msg = out_q.get_nowait()
    except queue.Empty:
        break
    print(msg)
