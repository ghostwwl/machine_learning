# 特征提取

----------------------------------------------

- sklearn.feature_extraction 模块记录


## DictVectorizer 
- 字典特征提取器（有的是这么翻译）
- `sklearn.feature_extraction.DictVectorizer(dtype=<class 'numpy.float64'>, separator='=', sparse=True, sort=True)`
  
将<特征-值>映射转化为向量。字典类型的对象转化为numpy.array或者scipy.sparse
特征值为string类型时，向量表示为one-hot二元编码，出现的string为1，其余为0.
特征值为int等数字类型时，对应的值为相应的数字。

### 构造函数说明：  
- dtype:特征值的类型。
- separator:可选，string。当特征值为string时，用来连接特征名称和值的符号，默认为'='。
例，当特征名为'f',而特征值含有'pam'和'spam'时，one-hot对应的向量名为'f=pam'和'f=spam'
- sparse:boolean,可选。默认为True,转换过程中生成一个scipy.sparse矩阵。当数据多表示为one-hot
类型时，占用内存过大，稀疏表示可以节约大量空间。
- sort:boolean,可选，默认为True。转化完成后对feature_names_和vocabulary_按字典序排列。

### 属性：  
- feature_names_:长度为n_features的列表，含有所有特征名称.
- vocabulary_:字典类型，特征名映射到特征在list中的index的字典对象

### 例如：

```text
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)
d = [{'foo':1,'bar':2},{'foo':3,'orz':1}]
x = v.fit_transform(d)
print(x)
#[[2. 1. 0.]
 [0. 3. 1.]]
print(v.feature_names_)
#['bar', 'foo', 'orz']
print(v.vocabulary_)
#{'foo': 1, 'bar': 0, 'orz': 2}

```


### 方法：  

- fit(X,y=None):   
学习一个将特征名称映射到索引的列表，返回值是其自身(DictVectorizer)

```text
v = DictVectorizer(sparse=False)
d = [{'foo':1,'bar':2},{'foo':3,'orz':1}]
print(v.fit(d))
#DictVectorizer(dtype=<class 'numpy.float64'>, separator='=', sort=True,sparse=False)
```

- fit_transform(X,y=None):  
学习一个将特征名称映射到索引的列表，返回值是为对应的特征向量，
一般2维 等价于fit(X).transform(X)

```text
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)
d = [{'foo':1,'bar':2},{'foo':3,'orz':1}]
print(v.fit_transform(d))
#[[2. 1. 0.]
 [0. 3. 1.]]
```

- get_feature_names():  
返回一个含有特征名称的列表，通过索引排序，如果含有one-hot表示的特征，则显示相应的特征名

```text
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)
d = [{'foo':'t1','bar':2},{'foo':'t2','orz':1}]
v.fit_transform(d)
print(v.get_feature_names())
#['bar', 'foo=t1', 'foo=t2', 'orz']
```

- get_params(deep=True):  
返回模型的参数（string到任何类型的映射）

```text
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)
d = [{'foo':'t1','bar':2},{'foo':'t2','orz':1}]
v.fit_transform(d)
print(v.get_params())
#{'dtype': <class 'numpy.float64'>, 'separator': '=', 'sort': True, 'sparse': False}
```

- inverse_transform(X,dict_type=<class 'dict'>):  
将转化好的特征向量恢复到转化之前的表示状态。X必须是通过transform或者fit_transform生成的向量。
X:shape(n_samples,n_features)
返回字典对象的列表，长度为n_samples。
```
from sklearn.feature_extraction import DictVectorizer
v = DictVectorizer(sparse=False)
d = [{'foo':'t1','bar':2},{'foo':'t2','orz':1}]
x = v.fit_transform(d)
print(v.inverse_transform(x))
#[{'bar': 2.0, 'foo=t1': 1.0}, {'foo=t2': 1.0, 'orz': 1.0}]
one-hot会被改为数值类型的特征而不能恢复原来的表示。
```

- restrict(support,indices=False):  
对支持使用特征选择的模型进行特征限制，例如只选择前几个特征  
support:矩阵类型，boolean或者索引列表，一般是feature selectors.get_support()的返回值。  
indices:boolean，可选，表示support是不是索引的列表 返回值是其自身(DictVectorizer)  
    
```text
>>> from sklearn.feature_extraction import DictVectorizer
>>> from sklearn.feature_selection import SelectKBest, chi2
>>> v = DictVectorizer()
>>> D = [{'foo': 1, 'bar': 2}, {'foo': 3, 'baz': 1}]
>>> X = v.fit_transform(D)
>>> support = SelectKBest(chi2, k=2).fit(X, [0, 1])
>>> v.get_feature_names()
['bar', 'baz', 'foo']
>>> v.restrict(support.get_support()) 
DictVectorizer(dtype=..., separator='=', sort=True,
        sparse=True)
>>> v.get_feature_names()
['bar', 'foo']
```

- set_params(**params):  
设置DictVectorizer的参数  

- transform(X):  
学习一个将特征名称映射到索引的列表，返回值是为对应的特征向量，一般2维


-------------------------------------

## FeatureHasher

- Hash特征提取器（直接对特征应用一个hash函数来决定特征在样本矩阵中的列索引）
- 采用哈希方法将象征性的特征序列转化为scipy.sparse矩阵，可以节约时间和空间。
- `sklearn.feature_extraction.FeatureHasher(n_features=1048576, input_type='dict', dytpe=<class 'numpy.float64'>, alternate_sign=True, non_negative=False)`
  
### 构造函数说明
- n_features:int,可选
    - 输出矩阵的特征个数（行数）  
- input_type:string,可选
    - 默认为'dict'  
    - 参数可为:'dict','pair' or string  
        - 'pair':(string,int)，string经过哈希映射，同一个string对应的int值相加作为特征值。  
        - string:(string,1)，类似于pair的int为1。  
        - dtype:numpy.type,可选，默认为np.float64  
特征值的类型  
- alternate_sign:boolean,可选
    - 默认True。 为True时为特征添加一个交替符号保存哈希空间的内积值。  
    - 可以近似看作随机稀疏化。  
- non_negative:boolean,可选
    - 默认False  
    - 为True时特征矩阵必须为非负数。0.21版本时会删除
  
```text
>>> from sklearn.feature_extraction import FeatureHasher
>>> h = FeatureHasher(n_features=10)
>>> D = [{'dog': 1, 'cat':2, 'elephant':4},{'dog': 2, 'run': 5}]
>>> f = h.transform(D)
>>> f.toarray()
array([[ 0.,  0., -4., -1.,  0.,  0.,  0.,  0.,  0.,  2.],
       [ 0.,  0.,  0., -2., -5.,  0.,  0.,  0.,  0.,  0.]])
```

### 方法：  
- fit([X,y]):  
    - 什么都不干233，存在是为了保证scikit-learn transformer API的完整性  
- fit_transform(X[,y]):  
    - X:shape(n_samples,n_features)的numpy矩阵，训练集  
    - y:shape(n_samples,)的numpy矩阵，目标值  
    - 返回X_new:shape(n_samples,n_features_new)的numpy矩阵，转化后的矩阵  
- get_params(deep=True)  
- set_params(**params)  
- transform(raw_X)  
    - 用法和DictVectorizer类似  


## CountVectorizer
- 将文本文档的集和转化为表示单词数量的矩阵，采用scipy.sparse.csr_matrix构造稀疏表示。
- `sklearn.feature_extraction.text.CountVectorizer(input='content',encoding='utf-8', decode_error='strict',strip_accents=None,lowercase=True,preprocessor=None,tokenizer=None, stop_words=None,token_pattern='(?u)\b\w\w+\b',ngram_range=(1,1),analyzer='word',max_df=1.0, min_df=1,max_features=None,vocabulary=None,binary=False,dtype=<class 'numpy.int64'>)`  
  
###　构造函数：  
- input:string{'filename','file','content'}  
    - filename:使用fit方法的参数是一个文件路径的列表集和，自动读入list中所有文件内容。  
    - file:fit的参数是一个文件路径，且该文件可读  
    - content:fit的参数是string或者bytes，即要处理的文本  
- encoding:string，默认utf-8
    - 文本编码  
- decode_error:{'strict','ignore','replace'}
    - 超出编码范围(上面参数给定的encoding)的字符处理方式
    - strict抛出编码错误异常，ignore为忽略.  
- strip_accents:{'ascii','unicode',None}  
    - 预处理时去掉口音，应该是一些俗语。ascii只在ASCII编码的字符上操作，速度快。unicode用于任何字符，速度较慢。None不进行操作  
- analyzer:string,{'word','char','char_wb'}  
    - 特征被分为word还是n-grams.char_wb只从文本范围内产生n-grams.

- preprocessor:callable or None(默认)  
    - 重载预处理过程  
- tokenizer:callable or None(默认)  
    - 重载字符串的标记化步骤。只在analyzer=='word'时有效  
- ngram_range:tuple(min_n,max_n)  
    - 参数为元组，满足min_n<=n<=max_n的n会产生相应的n-grams。  
- stop_words:'english',list or None(默认)  
    - english:使用英语中的停用词  
    - list:含有停用词的list集合，所有在list中的单词会被删除。只在analyzer=='word'时有效  
    - None:不会删除停用词。max_df被设置为[0.7,1.0)的值根据单词在文本中出现的频率自动滤除停用词。  
- lowercase:boolean,True（默认）。
    - 将所有字符变为小写  
- token_pattern:string  
    - 指示构成单词形式的正则表达式，只在analyzer=='word'时有效。
    - 例如默认的(?u)\b\w\w+\b表示两个字母及以上的会被当作单词，标点符号视作单词分隔符  
- max_df:float in range[0.0,1.0]或者int ,
    - 默认=1  
    - 建立单词表时，忽略频率严格大于给定阀值的项。
        - float表示比率
        - int表示数量  
- min_df:float in range[0.0,1.0]或者int ,默认=1  
    - 建立单词表时，忽略频率严格小于给定阀值的项。
        - float表示比率
        - int表示数量  
- max_features:int or None(默认)  
    - int时建立单词表只选择按出现频率的top max_features个项。
    - vocabulary不是None时忽略  
- vocabulary:可选
    - 映射或迭代器  
    - 映射:如字典类型，keys是单词，value是在特征矩阵中的索引.  
    - None时单词表由输入文本决定。  
- binary:boolean
    - 默认False  
    - 为True时所有非零项设为1，表示其出现过而不是统计出现次数。  
- dtype:type,可选  
    - 设定fit_transform()或transfrom()的返回矩阵类型
      
```text
>>> ngram_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(5, 5))
>>> ngram_vectorizer.fit_transform(['jumpy fox'])
...                                
<1x4 sparse matrix of type '<... 'numpy.int64'>'
   with 4 stored elements in Compressed Sparse ... format>
>>> ngram_vectorizer.get_feature_names() == (
...     [' fox ', ' jump', 'jumpy', 'umpy '])
True
>>> ngram_vectorizer = CountVectorizer(analyzer='char', ngram_range=(5, 5))
>>> ngram_vectorizer.fit_transform(['jumpy fox'])
...                                
<1x5 sparse matrix of type '<... 'numpy.int64'>'
    with 5 stored elements in Compressed Sparse ... format>
>>> ngram_vectorizer.get_feature_names() == (
...     ['jumpy', 'mpy f', 'py fo', 'umpy ', 'y fox'])
True
```
  
### 属性：  
- vocabulary_:字典类型，单词到特征索引的映射  
- stop_words_:集合，识别出的停用词集合.

  
### 方法：  
- build_analyzer()
    - 返回一个处理预处理和词语切分的调用  
- build_preprocessor()
    - 返回一个词语切分前预处理文本的函数  
- build_tokenizer()
    - 返回一个将字符串分成词语序列的函数  
- decode(doc)
    - 将输入编码为unicode字符串，编码方式取决于向量化参数  
- fit(raw_documents,y=None)
    - 从原始文档中学习一个包含所有单词的词汇表字典  
- raw_documents
    - 一个str,unicode或文件对象的迭代器  返回自身  
- fit_transform(raw_documents,y=None)
    - 学习一个词汇表字典返回一个文档-单词的矩阵，shape(n_samples,n_featrues)  
    - 相当于fit.transform,但是效率更高  
- raw_documents
    - 一个str,unicode或文件对象的迭代器  
- get_feature_names()
    - 特征索引到特征名称的映射  
- get_params(deep=True)  
    - 获取模型的参数。  
- get_stop_words()
    - 建立有效的停用词表  
- inverse_transform(X)
    - 将非零矩阵X恢复到每个文档的terms表示  
    - X:{array,sparse matrix},shape(n_samples,n_features)  
    - 返回值X_inv:矩阵列表，长度为n_samples  
- set_params(**params)
    - 设置参数，返回设置好的模型  
- transform(raw_documents)
    - 将文档转化为文档-单词矩阵。  


---------------------------------------------------------

## TfidfTransformer

- Tfidf特征提取器
- `sklearn.feature_extraction.text.TfidfTransformer(norm='l2',use_idf=True,smooth_idf=True,sublinear_idf=False)`

首先来介绍tf-idf：由于很多出现的高频词例如a,the会携带较少信息甚至不包含信息，但他们的数量较大，分类问题中  
会对结果产生较大的影响，tf-idf是一种对特征重新赋权值的方法。  
tf-idf(t,d) = tf(t,d)*idf(t)  
tf是词频term frequency,表示词条t在文档d中的出现频率。  
idf是逆向文件频率inverse document frequency，如果包含词条t的文档越少，idf越大，说明词条t携带的信息较多，具有很好的分类能力。  


### 构造特征提取器
- norm:'l1','l2' or None
    - 选择标准化词条向量的方式  
- use_idf:boolean,True（默认）
    - 使用idf重新计算权值  
- smooth_idf:boolean,True(默认)  
    - idf(d, t) = log [ n / df(d, t) ] + 1 (smooth_idf=False)  
    - idf(d, t) = log [ (1 + n) / (1 + df(d, t)) ] + 1.(smooth_idf=True)  
    - n是文档总数量，df(d,t)是文档频率(包含词条t的文档频率)  
- sublinear_tf:boolean,False(默认)  
    - 对tf进行次线性变化，例如tf=1+log(tf)  

### 方法
- fit(X[,y])
    - 学习idf向量  
    - X:稀疏矩阵,shape(n_samples,n_features),表示词条数量  
- fit_transform(X,y=None,**fit_params):  
    - 学习权值然后转化为tf-idf向量  
    - X:训练集合,shape(n_samples,n_features)  
    - y:目标值,shape(n_samples,)  
    - 返回X_new:shape(n_samples,n_features_new),经转换的矩阵  
- get_params(deep=True)获取参数  
- set_params(**params)设置参数  
- transform(X,copy=True):  
    - 将数量矩阵转化为tf或tf-idf表示  
    - X:稀疏矩阵,shape(n_samples,n_features)  
    - copy:boolean,True(默认)。操作时进行深度复制.copy()还是使用引用  
    - 返回向量:稀疏矩阵shape(n_samples,n_features)  


-------------------------------------------------------------------------------

## TfidfVectorizer
- TF-IDF特征提取
- `sklearn.feature_extraction.text.TfidfVectorizer(input=’content’, encoding=’utf-8’, decode_error=’strict’, strip_accents=None, lowercase=True, preprocessor=None, tokenizer=None, analyzer=’word’, stop_words=None, token_pattern=’(?u)\b\w\w+\b’, ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False, dtype=<class ‘numpy.int64’>, norm=’l2’, use_idf=True, smooth_idf=True, sublinear_tf=False)`
- 先由CountVectorizer进行词频统计，然后TfidfTransformer进行转化。参数含义参考上述CountVectorizer、TfidfTransformer

### 和　TfidfTransformer　的关系
```
vectorizer=CountVectorizer()
transformer=TfidfTransformer()
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
等价于：
transformer=TfidfVectorizer()
tfidf2=transformer.fit_transform(corpus)
```

### 属性：
- vocabulary_
    - 词条到特征索引的映射，字典类型
- idf_
    - use_idf==True时为学习到的idf向量，否则为None
- sopt_words_
    - 停用词集合
方法参考CountVectorizer、TfidfTransformer，二者的方法都有


-------------------------------------------------------------------------------


## image.extract_patches_2d 
- `sklearn.feature_extraction.image.extract_patches_2d(image,patch_size,max_patches=None,random_state=None)`
- 将二维图片重新表示为小块的集合。

### 构造函数说明
- image:矩阵
    - shape(image_height,image_width)或者(image_height,image_width,n_channels) 
    - n_channels==3时采用RGB表示
- patch_size:元组(patch_height,patch_width)，均为int。
    - 一块的维数。
- max_patches:int,float，默认为None.提取出的块数的最大数量，float表示所占比例,(0,1)
    - 返回值：矩阵,shape(n_patches,patch_height,patch_width)或者shape(n_patches,patch_height,patch_width,n_channels)
    
```text

>>> from sklearn.feature_extraction import image
>>> one_image = np.arange(16).reshape((4, 4))
>>> one_image
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11],
       [12, 13, 14, 15]])
>>> patches = image.extract_patches_2d(one_image, (2, 2))
>>> print(patches.shape)
(9, 2, 2)
>>> patches[0]
array([[0, 1],
       [4, 5]])
>>> patches[1]
array([[1, 2],
       [5, 6]])

```


-------------------------------------------------------------------------------


## image.PatchExtractor
- 参数同 image.extract_patches_2d
- `sklearn.feature_extraction.image.PatchExtractor(patch_size=None,max_patches=None,random_state=None)`

### 方法：
- fit(X[,y])
    - 没有任何功能，返回自身
- get_params(deep=True)
    - 获取参数
- set_params(**params)
    - 设置参数
- transform(X):
    - 将图片样本X转化为小块数据矩阵
    - X : array, shape = (n_samples, image_height, image_width) or(n_samples, image_height, image_width, n_channels)
    - 返回值patches : array, shape = (n_patches, patch_height, patch_width) or(n_patches, patch_height, patch_width, n_channels)
