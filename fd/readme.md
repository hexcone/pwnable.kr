# pwnable.kr: fd

```len = read(fd, buf, 32);```
Each process have 3 file descriptor: [0] stdin, [1] stdout and [3] stderr [https://en.wikipedia.org/wiki/File_descriptor]. In the case, we want to read from one of these stream, such that the value is "LETMEWIN\n". 

```int fd = atoi( argv[1] ) - 0x1234;```
To read from stdin, we want to set the value of fd to 0. 0x1234 in integer will be 4660 and this will be our parameter to pass in. After which, we input the string "LETMEWIN\n" to arrive at the flag.

```
$ ./fd 4660
LETMEWIN
```