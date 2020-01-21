/*

int print_in_binary(int num1)
{
	printf("2진수 표현 : ");
	for (int i = 7; i >= 0; --i)
	{
		printf("%d", (num1 >> i) & 1);
	}
	printf("\n");
	return 0;
}


*/

#include <stdio.h>

int print_in_binary(int num1);

int main()
{
	struct strct
	{
		unsigned int a : 3;
		unsigned int b : 7;
	};

	struct strct data;

	data.a = 15;
	data.b = 255;

	printf("비트필드를 사용하여 3비트 지정한 멤버변수 a 값 : %d\n", data.a);
	print_in_binary(data.a);
	printf("비트필드를 사용하여 7비트 지정한 멤버변수 a 값 : %d\n", data.b);
	print_in_binary(data.b);
}

int print_in_binary(int num1)
{
	printf("2진수 표현 : ");
	for (int i = 7; i >= 0; --i)
	{
		printf("%d", (num1 >> i) & 1);
	}
	printf("\n");
	return 0;
}
