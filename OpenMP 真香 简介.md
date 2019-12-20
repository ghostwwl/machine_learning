### OpenMP（Open MultiProcessing）

- OpenMP是作为共享存储标准而问世的。它是为在多处理机上编写并行程序而设计的一个应用编程接口。它包括一套编译指导语句和一个用来支持它的函数库
    - 在项目程序已经完成好的情况下不需要大幅度的修改源代码，只需要加上专用的pragma来指明自己的意图，由此编译器可以自动将程序进行并行化，
    并在必要之处加入同步互斥以及通信。当选择忽略这些pragma，或者编译器不支持OpenMp时，程序又可退化为通常的程序(一般为串行)，代码仍然可以正常运作，
    只是不能利用多线程来加速程序执行。OpenMP提供的这种对于并行描述的高层抽象降低了并行编程的难度和复杂度，这样程序员可以把更多的精力投入到并行算法本身，
    而非其具体实现细节。对基于数据分集的多线程程序设计，OpenMP是一个很好的选择。
    
    - OpenMP支持的语言包括C/C++、Fortran；而支持OpenMP的编译器VS、gcc、clang等都行。可移植性也很好：Unix/Linux和Windows
- 为什么不用 pthread， 因为它更简单， 看下面的 就已经并行了 简单吧
    - 看那一句 `#pragma omp parallel for` 就并行了 
    - 指定线程数目 `#pragma omp parallel for num_threads(4)`
    
```
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

void Test (int n) 
{
	for(int i = 0; i < 10000; ++i) {
		//do nothing, just waste time
	}
	printf("%d, ", n);
}

int main(int argc, char* argv[]) 
{

	#pragma omp parallel for
	for(int i = 0; i < 50; ++i)
		Test( i );
	system("pause");

}


void do_sum()
{
    int sum = 0;
    #pragma omp parallel for num_threads(32) reduction(+:sum)
    for(int i=0; i<100; i++)
    {
        sum +=  i; 
    }

    cout << sum << endl;
    
}


void do_sum2()
{
    int sum = 0; 
#pragma omp parallel  num_threads(3) 
    {
#pragma omp atomic 
sum += 10; 
    
#pragma omp barrier  // TODO : disable this to see 
cout << sum << endl; 
}
}


``` 

- 到这里可以说 OpenMP 真香 历史代码改并行的神器啊
- [OpenMP用法大全](https://www.cnblogs.com/jfdwd/p/10960544.html)
