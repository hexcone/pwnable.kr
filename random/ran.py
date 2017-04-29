#!/usr/bin/python

from pwn import *

# open connection
s = ssh(host='pwnable.kr',
    user='random',
    port=2222,
    password='guest')
sh = s.process('./random')

# prepare payload
ran = 1804289383 & 0xffffffff
result = 3735928559 & 0xffffffff #0xdeadbeef
key = ran ^ result
print 'Payload: ', str(key)

# send payload
sh.sendline(str(key))
print sh.recvline()
print sh.recvline()
