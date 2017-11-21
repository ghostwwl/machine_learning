### 常用的awk文本处理

+ 假设标本格式为：
>kind\ttitle


#### 1. 统计标本分布
>cat xxx.txt |awk -F "\t" '{cropus[$1]++}END{for (kind in cropus) print kind "\t" cropus[kind]}'|sort -n -k 2 -t $'\t'

#### 2. 正文按照单字分词
>cat xxx.txt|awk -F "\t" '{r="";l=length($2);i=1;do{r=(r" "substr($2, i, 1));i=i+1;} while (i <= l)} {print ($1" , , "r);}'|tr -s  "[ ]+" " "
```
1. 取字符串长度 然后 逐个截取 加上空格拼接
2. tr 把两个及两个以上的空格 替换为单个空格
```

#### 3. 对某个kind的标本随机抽取10条
>cat xxx.txt|awk -F "\t" '$2==xxxx{print $0;}'|shuf -n 10

#### 4. 选取文本里 文本字符小于5的标本
>cat xxx.txt|awk -F "\t" length($2)<5 {print $0}


+ 假设标本格式为：
>kind\t词1 词2 词2


#### 按照空格分割 如果标本分词后 只有单个词的 打印出标本的行号和标本
>cat x.corpus|awk '{corpus_len=split($0, a, " ");if(corpus_len<3)print  "line:" NR " " $0;}'
#### 按照空格分割 如果标本分词后 只有单个词的 打印标本里的唯一词条
>cat x.corpus|awk '{corpus_len=split($0, a, " ");if(corpus_len<3)print  "line:" NR " " a[2];}'
#### 按照空格分割标本 如果标本只包含一个词并且这个词是单个数字或字母字符的 打印出标本的行号和标本
>cat x.corpus|awk '{corpus_len=split($0, a, " ");if(corpus_len<3 && a[2] ~ /^[0-9a-zA-Z]{1}$/)print  "line:" NR " " $0;}'
#### 标本里所有英文转小写
>cat x.corpus|tr "[:upper:]" "[:lower:]"


+ 还有标本分割 自己去百度split呢
