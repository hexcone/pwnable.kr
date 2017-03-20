# pwnable.kr: col

In this program, we pass in a 20 bytes argument. check_password() then add up 5 blocks of 4 bytes each and return the result.

```
if(hashcode == check_password( argv[1] )){
	system("/bin/cat flag");
		return 0;
}
```
The program then check that the returned value is equals to the hashcode of 0x21DD09EC.

We construct 5 values, such that their summation is equals to 0x21DD09EC. 0x21DD09EC = 0x15ac2f4 + 0x15ac2f4 + 0x15ac2f4 + 0x15ac2f4 + 1c71fe1c. And concatenate them.

```
char test[] = "\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1c\x71\xfe\x1c";
printf("Input: %s\n", test);
```
First, I tried to print out the char in cal.c and copy paste the output to the argument, but it doesn't work :(

This will print out the char representation of the hex value instead.
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