
# coo/csc/csr稀疏矩阵存储原理--实例

- coo 压缩算法
- csc 压缩算法
- csr 压缩算法



## coo 压缩算法

- 用例：
```text

	1	0	4
	0	3	5
	2	0	6
```



- 数据结构：
    - 行数
    - 列数
    - rowinx
    - colinx
    - values
    
- 推导过程:

```text
a = Array(0, 0, 1, 1, 2, 2)     --> rowinx     --> 每一行上，非零位置的行号
b = Array(0, 2, 1, 2, 0, 2)     --> colinx     --> 每一列上，非零位置的列号
c = Array(1, 4, 3, 5, 2, 6)     --> values     --> 每一行上所有非零的数字依次放入


c[0] --> 位置 (a[0], b[0]) --> (0, 0) --> 1
c[1] --> 位置 (a[1], b[1]) --> (0, 2) --> 4
c[2] --> 位置 (a[2], b[2]) --> (1, 1) --> 3
c[3] --> 位置 (a[3], b[3]) --> (1, 2) --> 5
c[4] --> 位置 (a[4], b[4]) --> (2, 0) --> 2
c[5] --> 位置 (a[5], b[5]) --> (2, 2) --> 6


```

## csr 压缩算法

- 用例：
```text

	1	0	4
	0	3	5
	2	0	6
```




- 数据结构：
    - 行数
    - 列数
    - rowPtrs
    - colIndices
    - values
    
    
- 推导过程:

```text
a = Array(0, 2, 4, 6)           --> rowPtrs     --> 第一个元素一直是0, 第二个元素是第一行的非零元素的数量, 后续的值为前一个值 + 下一行非零元素的数量
b = Array(0, 2, 1, 2, 0, 2)     --> colIndices  --> 每一列上 非零位置的行号
c = Array(1, 4, 3, 5, 2, 6)     --> values      --> 每一行上所有非零的数字依次放入

第一行的值： c[ a[0]: a[1] ] --> c[ 0: 2] --> Array(1, 4)
第一行的值的位置: b[ a[0]: a[1] ] --> b[ 0: 2] --> Array(0, 2)
第一行的非零结果:
    (0, 0) --> 1
    (0, 2) --> 4
    
第一行的值： c[ a[1]: a[2] ] --> c[ 2: 4] --> Array(3, 5)
第二行的值的位置: b[ a[2]: a[3] ] --> b[ 2: 4] --> Array(1, 2)
第二行的非零结果:
    (1, 1) --> 3
    (1, 2) --> 5
    
第一行的值： c[ a[2]: a[3] ] --> c[ 4: 6] --> Array(2, 6)
第三行的值的位置: b[ a[2]: a[3] ] --> b[ 4: 6] --> Array(0, 2)
第三行的非零结果:
    (2, 0) --> 2
    (2, 2) --> 6

```


	
## csc 压缩算法

- 用例：
```text

	1	0	4
	0	3	5
	2	0	6
```



- 数据结构：
    - 行数
    - 列数
    - colPtrs
    - rowIndices
    - values

- 推倒过程:

```text
a =	Array(0, 2, 3, 6)         --> colPtrs     --> 第一个元素一直是0, 第二个元素是第一列的非零元素的数量, 后续的值为前一个值 + 下一列非零元素的数量
b =	Array(0, 2, 1, 0, 1, 2)   --> rowIndices  --> 每一列上 非零位置的行号
c =	Array(1, 2, 3, 4, 5, 6)   --> values      --> 每一列上所有非零的数字依次放入

第一列的值： c[ a[0]: a[1] ] --> c[0:2] --> Array(1, 2)
第一列值的位置: b[ a[0]: a[1] ] --> b[0:2] --> Array(0, 2) --> (0,0), (2, 0)
第一列的非零结果:
    (0, 0) --> 1
    (2, 0) --> 2
    
第二列的值: c[ a[1]: a[2] ] --> c[2:3] --> Array(3)
第二列的值的位置: b[ a[1]: a[2] ] --> b[2:3] --> Array(1) --> (1,1)
第二列的非零结果:
    (1, 1) --> 3
    
第三列的值: c[ a[2]: a[3] ] --> c[3:6] --> Array(4, 5, 6)
第三列的值的位置: b[ a[2]: a[3] ] --> b[3:6] --> Array(0, 1, 2)
第三列的非零结果:    
    (0, 2) --> 4
    (1, 2) --> 5
    (2, 2) --> 6
    
```



### 相关测试

- python 的 scipy.sparse 已经实现

```python

from scipy.sparse import *
import numpy as np
row = [0, 0, 1, 1, 2, 2]
col = [0, 2, 1, 2, 0, 2]
data = [1, 4, 3, 5, 2, 6]
coo = coo_matrix((data,(row,col)),shape=(3,3),dtype=np.int)

print(coo)
print(coo.todense())



row_ptr = [0, 2, 4, 6]
col = [0, 2, 1, 2, 0, 2]
data = [1, 4, 3, 5, 2, 6]
csr = csr_matrix((data,col,row_ptr),shape=(3,3),dtype=np.int)# 被压缩的数组放在最后一个
csr.todense()

print(coo)
print(coo.todense())


col_ptr = [0, 2, 3, 6]
row = [0, 2, 1, 0, 1, 2]
data = [1, 2, 3, 4, 5, 6]
csc = csc_matrix((data,row,col_ptr),shape=(3,3),dtype=np.int)# 被压缩的数组放在最后一个

print(csc)
print(csc.todense())

```
	
- spark 的 mllib 里有 csc 的实现
```scala
import org.apache.spark.mllib.linalg.{Matrix,Matrices}

val sm: Matrix=Matrices.sparse(3, 3, Array(0, 2, 3, 6), Array(0, 2, 1, 0, 1, 2), Array(1, 2, 3, 4, 5, 6))

```
