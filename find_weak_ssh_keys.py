#!/usr/bin/env python
"""
    Wed Dec 30 10:49:47 AM 2020 CST
    find weak keys

    nothing fancy, but effective at finding weak ssh keys

"""
import paramiko
import socket
import sys

keys = {}

for arg in sys.argv[1:]:
    sock = socket.socket()
    sock.connect((arg, 22))
    trans = paramiko.transport.Transport(sock)
    trans.start_client()
    k = trans.get_remote_server_key()
    keys.setdefault("host", sys.argv[1])
    keys.setdefault("key_size", trans.host_key.size)
    keys.setdefault("key_type", trans.host_key_type)
    keys.setdefault("key_base64", k.get_base64())
    print(keys)
