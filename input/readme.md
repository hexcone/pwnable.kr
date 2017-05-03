# pwnable.kr: random

After logging in, we do a ```ls``` and observe the below files
```
$ ls
flag  input  input.c
```

Looking at input.c, the flow of the program is as follows
1. To clear stage 1, we must pass in 100 arguments, argv['A'] must equates "\x00" and argv['B'] must equates "\x20\x0a\x0d". argv['A'] and argv['B'] are argv[65] and argv[66] respectively.
2. To clear stage 2, the 4 bytes read from fd=0 must be "\x00\x0a\x00\xff" and 4 bytes read from fd=2 must be "\x00\x0a\x02\xff"
3. To clear stage 3, there must be an environment variable of '\xde\xad\xbe\xef'='\xca\xfe\xba\xbe'
4. To clear stage 4, there should be a file named '\x0a' in the local directory, and it should contains '\x00\x00\x00\x00'.
5. For stage 5, it starts a socket with argv['C'], which is argv[67], as the port number. It then blocks and wait to accept a connection from a client. The client will then have to send 4 bytes of '\xde\xad\xbe\xef'.

For stage 1, we form our cmd and arguments respectively as such. (The cmd below is an example, doesn't work, run the python script instead)
```
echo -e '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 \x00 \x20\x0a\x0d 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99' | ./input
```

For stage 2, to write to fd=0, we can peform a sendline(). To write to fd=2, the pwntools allows us to provide an argument to define stderr, hence, we set this to fd=0 (stdin) as well. After which, we send the 2 string of 4 bytes to standard input.
```
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin)
...
sh.sendline('\x00\x0a\x00\xff\x00\x0a\x02\xff')
```

For stage 3, we set the necessary values in a dictionary, and pass it as an argument when executing the program
```
env = {}
env['\xde\xad\xbe\xef'] = '\xca\xfe\xba\xbe'
...
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin, env=env)
```

For stage 4, we cannot create a file in the /home/input2/ directory that we are originally in, but we can do so in /tmp/. Hence, when we connect via ssh, we change directory to /tmp/ and create the required file, before calling the input program via its full path.
```
create_file = 'cd /tmp; echo -ne "\x00\x00\x00\x00" > "\n";'
s.run_to_end(create_file)
sh = s.process(argv=cmd, stdin=sys.stdin, stderr=sys.stdin, env=env, cwd='/tmp')
```
If the above doesn't work, (lol actually it doesn't), we can ssh in manually to create the required file on /tmp
```
cd /tmp;
echo -ne "\x00\x00\x00\x00" > "
";
cat "
";
```

Stage 5, I attempted to connect from our python script as such. However, I received a 111 Connection refused.
```
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = -1
while (result != 0):
    result = client.connect_ex((socket.gethostbyname('pwnable.kr'), socket_port))
    print result
client.send('\xde\xad\xbe\xef')
```
Hence, let's attempt to connect to the socket locally instead.
```
send_to_socket = 'echo -ne "\xde\xad\xbe\xef" | nc localhost ' + str(socket_port)
...
s.run_to_end(send_to_socket)
```

We have cleared all 5 stages, however, since our program runs in a separate directory from the flag file... it is unable to print out the flag lol. Below we create a symbolic link to the actual flag. If it doesn't work.. ssh in to run manually lol
```
cd /tmp
ln -sf /home/input2/flag /tmp/flag
```

The link flag now exist, but our program get a permission denied as it try to follow it. Instead of /tmp, we move everything to /tmp/rawr to run. Creating the file in stage 4 in /tmp/rawr as well.
```
$ ./input.py
Welcome to pwnable.kr

Let's see if you know how to give input to program

Just give me correct inputs then you will get the flag :)

Stage 1 clear!

Stage 2 clear!

Stage 3 clear!

Stage 4 clear!

Stage 5 clear!

Mommy! I learned how to pass various input in Linux :)

```