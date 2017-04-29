# pwnable.kr: random

After logging in, we do a ```ls``` and observe the below files
```
$ ls
flag  random  random.c
```

The flow of the program random is as follows
1. Generate a random value with ```rand()```
2. Prompt for a key input
3. Check that the random value XOR our key gives us 0xdeadbeef
4. If the check succeeds, it prints out the flag for us

If we compile the same program with a printf to see the random value, we observe that the random value is always the same
```
user@ubuntu:~/Desktop$ ./random
1804289383
^C
user@ubuntu:~/Desktop$ ./random
1804289383
^C
user@ubuntu:~/Desktop$ ./random
1804289383
^C
```

This is because, when rand() is not initialized with a seed, it is automatically seeded with a value of 1.

The value of key would be the XOR of 0xdeadbeef and the random value we observe above

Running ran.py, we get
```
./ran.py
Payload:  3039230856
Payload:  3039230856
Good!

Mommy, I thought libc random is unpredictable...
```