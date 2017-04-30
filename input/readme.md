# pwnable.kr: random

After logging in, we do a ```ls``` and observe the below files
```
$ ls
flag  input  input.c
```

Looking at input.c, the flow of the program is as follows
1. To clear stage 1, we must pass in 100 arguments, argv['A'] must equates "\x00" and argv['B'] must equates "\x20\x0a\x0d". argv['A'] and argv['B'] are argv[65] and argv[66] respectively.
2. 
3. 
4. 