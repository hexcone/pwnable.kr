# pwnable.kr: flag

We run the program and it prints out
```
$ ./flag
I will malloc() and strcpy the flag there. take it.
```

The output give us a hint that ```malloc```, and ```strcpy``` is called. Let's try replacing ```strcpy``` with our own version.
```
/* strcpy.c*/
#include <string.h>
#include <stdio.h>

char *strcpy(char *dest, const char *src)
{
	char *d = dest;
	while (*src) {
		*d = *src;
		d++;
		src++;
	}
	printf("Flag: \"%s\"", dest);

	return (dest);
}
```

Compile it and run
```
$ gcc -shared -fPIC -o strcpy.so strcpy.c
$ LD_PRELOAD=$PWD/strcpy.so ./flag
```
But it doesn't work, so I added another definition if it is using ```strncpy```, but no output from there either, seems like both methods are not called? :(

```
$ file flag
flag: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, stripped
$ strings flag
...
su`"]R
UPX!
UPX!
```
When we run the above, we don't get any obvious flag, everything is mostly unreadable, but we notice "UPX!" towards the end.

Is it I finally caught the hint of "Papa brought me a packed present! let's open it."? Let's unpack it
```
$ sudo apt-get install upx-ucl
$ upx -d flag
$ strings flag > output
```

Scrolling through the ouput, we find the flag
```
...
UPX...? sounds like a delivery service :)
I will malloc() and strcpy the flag there. take it.
...
```