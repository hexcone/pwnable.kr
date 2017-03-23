# pwnable.kr: col

In this program,
1. we pass in a 20 bytes value
2. in check_password(), it splits the value into 5 blocks of 4 bytes each
3. perform summation of the 5 new values and return the result.
4. the result is compared with 0x21DD09EC, if it match, we get the key

We construct 5 values, such that their summation is equals to 0x21DD09EC. 0x21DD09EC = 0x15ac2f4 + 0x15ac2f4 + 0x15ac2f4 + 0x15ac2f4 + 1c71fe1c. And concatenate them.
```
char test[] = "\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1c\x71\xfe\x1c";
printf("Input: %s\n", test);
```

First, I tried to print out the char in cal.c and copy paste the output to the argument, but it doesn't work :(

This will print out the char representation directly to the console instead.
```
$ echo -e "\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1c\x71\xfe\x1c" | awk '{printf "%s\n", $_}'
```

Supply this value to the program
```
$ ./col $(echo -e "\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1c\x71\xfe\x1c" | awk '{printf "%s\n", $_}')
```

But it doesn't work :( Endianness? Let's try flipping each block around.
```
$ ./col $(echo -e "\xf4\xc2\x5a\x1\xf4\xc2\x5a\x1\xf4\xc2\x5a\x1\xf4\xc2\x5a\x1\x1c\xfe\x71\x1c" | awk '{printf "%s\n", $_}')
daddy! I just managed to create a hash collision :)
```