# pwnable.kr: fd

In this program, 
1. It takes in an argument
2. 0x1234 is subtracted from the argument, to give us the value of fd
3. we then read from the file descriptor stream with the value corresponding to fd
4. and store the value from the stream to buf
5. we compare the value of buf and "LETMEWIN\n", if it matches, we get the flag

Each process have 3 file descriptor: [0] stdin, [1] stdout and [2] stderr [https://en.wikipedia.org/wiki/File_descriptor]. In the case, we want to read from one of these stream, and stdin seems like the easiest.

```
int fd = atoi( argv[1] ) - 0x1234;
```
To read from stdin, we want to set the value of fd to 0. 0x1234 in integer will be 4660 and this will be our parameter to pass in. After which, we input the string "LETMEWIN\n" to arrive at the flag.

```
$ ./fd 4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```