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
5. 

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
If the above doesn't work, we can ssh in manually to create the required file on /tmp
```
echo -ne "\x00\x00\x00\x00" > "
";
cat "
";
```