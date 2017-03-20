#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;

int main(int argc, char* argv[]){
	char test[] = "\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1\x5a\xc2\xf4\x1c\x71\xfe\x1c";
	printf("Input: %s\n", test);
	
	return 0;
}
