# 使用 xpath 去解析京东最终页
这里用 lxml.etree 去处理xpath呢

## 不扯蛋 看码
```python
import re
import requests
from lxml import etree

r = requests.get('http://item.jd.com/29777449783.html')                                                                                                                        
goods = r.content.decode('gb18030', 'ignore')                                                                                                                                    
goods_info = etree.HTML(goods)  

```

## 获取当前sku的 color 属性
```python
# 使用xpath
# 选择 id为 choose-attr-1 的div --> 在他的所后代div里选择 class 属性 包含 selected 属性的 div --> 取这个div的 data-value属性值
goods_info.xpath('//div[@id="choose-attr-1"]/descendant::div[contains(@class, "selected")]/@data-value')[0] 

# 使用正则
# yanse --> 拼音等于 color 的意思
yanse = re.findall('(?s)<div id="choose-attr-1".*?class="item  selected  " data-sku="\d+" data-value="(.*?)">', goods)
if yanse:
    result = yanse[0]

```

## 获取当前sku的 size 属性
```python
# 参考上面自行脑补
goods_info.xpath('//div[@id="choose-attr-2"]/descendant::div[contains(@class, "selected")]/@data-value')[0]

# 使用正则
size = re.findall('(?s)<div id="choose-attr-2".*?class="item  selected  " data-sku="\d+" data-value="(.*?)">', goods)
if size:
    result = size[0]
```


## 哥要商品的 扩展属性 呢
```python

# 使用正则呢 自己去整

# xpath
print(goods_info.xpath('//div[@class="p-parameter"]/ul/li/descendant-or-self::*/text()'))

['品牌： ',
 '狼中花',
 '\n                                ',
 '\n                            ',
 '商品名称：保安服 特勤服 保安特勤服套装夏季短袖作训服套装黑色男特种作战服男女酒店物业门卫工作服套装包邮 斜纹夏长袖套装（送腰带+标志+帽子+袜子） 160/S',
 '商品编号：29777449783',
 '店铺： ',
 '狼中花运动户外旗舰店',
 '商品毛重：0.8kg',
 '商品产地：中国大陆',
 '货号：斜纹夏季特勤服套装',
 '尺码：S，M，L，XL，XXL，XXXL，XXXXL',
 '领型：翻领',
 '颜色：黑色',
 '材质：涤棉',
 '裤长：长裤',
 '袖长：短袖',
 '分类：迷彩作训服',
 '适用人群：男士',
 '功能：速干']
```
- 使用正则的时候 品牌没有获取到
- 注意 使用xpath的时候 `品牌` 和 `店铺` 这两个属性 是 li 下面 a 链里的文本


## 获取当前页面的路径
- ' 运动户外>户外鞋服>军迷服饰>狼中花 >保安服 特勤服 保安特勤服...' 这样的一坨
```python

goods_info.xpath('//div[@id="crumb-wrap"]/descendant::div[contains(@class, "item")]/a/text() | //div[@id="crumb-wrap"]/descendant::div[contains(@class, "ellipsis")]/@title')

```
- 选择 id 为 crumb-wrap 的div
    - 在他的所有后代元素的div里选取 class 包含 item 的div
        - 选择上面的div下面的 a链接 获取他的text 
        - 以上就会获取到 类目和品牌相关的导航信息  
            `['运动户外', '户外鞋服', '军迷服饰', '狼中花']`
    - 在他的所有后代元素的div里选取 class 包含 ellipsis 的div
        - 这个div的title 元素 就是商品标题
- 最终结果会获取到  
`['运动户外', '户外鞋服', '军迷服饰', '狼中花', '保安服 特勤服 保安特勤服套装夏季短袖作训服套装黑色男特种作战服男女酒店物业门卫工作服套装包邮 斜纹夏长袖套装（送腰带+标志+帽子+袜子） 160/S']`


--------------------------------------

## xpath 相关语法

#### 1、匹配某节点下的所有`.//`

//获取文档中所有匹配的节点，.获取当前节点，有的时候我们需要获取当前节点下的所有节点，.//一定要结合.使用//，否则都会获取整个文档的匹配结果.


#### 2、匹配包含某属性的所有的属性值//@lang
```python
print tree.xpath('//@code') #匹配所有带有code属性的属性值
```

#### 3、选取若干路径`|`

这个符号用于在一个xpath中写多个表达式用，用|分开，每个表达式互不干扰
```python
print tree.xpath('//div[@id="testid"]/h2/text() | //li[@data]/text()') #多个匹配条件
```

#### 4、 Axes（轴）

- `child：选取当前节点的所有子元素` 
```python
>>print tree.xpath('//div[@id="testid"]/child::ul/li/text()') #child子节点定位
>>print tree.xpath('//div[@id="testid"]/child::*') #child::*当前节点的所有子元素
>>#定位某节点下为ol的子节点下的所有节点
>>print tree.xpath('//div[@id="testid"]/child::ol/child::*/text()') 
```

- `attribute：选取当前节点的所有属性`
```python
>>print tree.xpath('//div/attribute::id') #attribute定位id属性值
>>print tree.xpath('//div[@id="testid"]/attribute::*') #定位当前节点的所有属性
```

- `ancestor：父辈元素 / ancestor-or-self：父辈元素及当前元素`
```python

>>print tree.xpath('//div[@id="testid"]/ancestor::div/@price') #定位父辈div元素的price属性
>>print tree.xpath('//div[@id="testid"]/ancestor::div') #所有父辈div元素
>>print tree.xpath('//div[@id="testid"]/ancestor-or-self::div') #所有父辈及当前节点div元素
>>[<Element div at 0x23fc108>]
>>[<Element div at 0x23fc108>, <Element div at 0x23fc0c8>]
```


- `descendant：后代 / descendant-or-self：后代及当前节点本身`

使用方法同上

- `following :选取文档中当前节点的结束标签之后的所有节点`
```python

#定位testid之后不包含id属性的div标签下所有的li中第一个li的text属性
>>print tree.xpath('//div[@id="testid"]/following::div[not(@id)]/.//li[1]/text()') 
```

- `namespace：选取当前节点的所有命名空间节点`
```python
>>print tree.xpath('//div[@id="testid"]/namespace::*') #选取命名空间节点
```


- `parent：选取当前节点的父节点`
```python
>>#选取data值为one的父节点的子节点中最后一个节点的值
>>print tree.xpath('//li[@data="one"]/parent::ol/li[last()]/text()') 
>>#注意这里的用法，parent::父节点的名字
```

- `preceding：选取文档中当前节点的开始标签之前的所有节点`
```python

>>#记住是标签开始之前，同级前节点及其子节点
>>print tree.xpath('//div[@id="testid"]/preceding::div/ul/li[1]/text()')[0] 
>>时间
>>#下面这两条可以看到其顺序是靠近testid节点的优先
>>print tree.xpath('//div[@id="testid"]/preceding::li[1]/text()')[0]
>>print tree.xpath('//div[@id="testid"]/preceding::li[3]/text()')[0]
>>任务
>>时间

```

- `preceding-sibling：选取当前节点之前的所有同级节点`
```python

>>#记住只能是同级节点
>>print tree.xpath('//div[@id="testid"]/preceding-sibling::div/ul/li[2]/text()')[0]
>>print tree.xpath('//div[@id="testid"]/preceding-sibling::li') #这里返回的就是空的了
>>地点
>>[]
```

- `self：选取当前节点`

```python
>>#选取带id属性值的div中包含data-h属性的标签的所有属性值
>>print tree.xpath('//div[@id]/self::div[@data-h]/attribute::*') 
>>['testid', 'first']
```

- 呵呵了

```python
#定位id值为testid下的ol下的li属性值data为two的父元素ol的兄弟前节点h2的text值
>>print tree.xpath('//*[@id="testid"]/ol/li[@data="two"]/parent::ol/preceding-sibling::h2/text()')[0] 
>>这里是个小标题
```

#### 5、position定位
```python
>>print tree.xpath('//*[@id="testid"]/ol/li[position()=2]/text()')[0] 
>>2
```

#### 6、条件
```python
>>定位所有h2标签中text值为`这里是个小标题`
>>print tree.xpath(u'//h2[text()="这里是个小标题"]/text()')[0]
>>这里是个小标题
```

#### 7、函数

- `count：统计`
```python
>>print tree.xpath('count(//li[@data])') #节点统计
>>3.0
```

- `concat：字符串连接`
```python
>>print tree.xpath('concat(//li[@data="one"]/text(),//li[@data="three"]/text())')
>>13
```

- `string：解析当前节点下的字符`
```python
>>#string只能解析匹配到的第一个节点下的值，也就是作用于list时只匹配第一个
>>print tree.xpath('string(//li)') 
>>时间
```

- `local-name：解析节点名称`
```python
>>print tree.xpath('local-name(//*[@id="testid"])') #local-name解析节点名称
>>div
```

- `contains(string1,string2)：如果 string1 包含 string2，则返回 true，否则返回 false`
```python
>>tree.xpath('//h3[contains(text(),"H3")]/a/text()')[0] #使用字符内容来辅助定位
>>百度一下

>>一记组合拳
>>#匹配带有href属性的a标签的先辈节点中的div，其兄弟节点中前一个div节点下ul下li中text属性包含“务”字的节点的值
>>print tree.xpath(u'//a[@href]/ancestor::div/preceding::div/ul/li[contains(text(),"务")]/text()')[0] 
>>任务
```

*注意：兄弟节点后一个节点可以使用：following-sibling*

- `not：布尔值（否）`
```python
>>print tree.xpath('count(//li[not(@data)])') #不包含data属性的li标签统计
>>18.0
```

- `string-length：返回指定字符串的长度`
```python
>>#string-length函数+local-name函数定位节点名长度小于2的元素
>>print tree.xpath('//*[string-length(local-name())<2]/text()')[0] 
>>百度一下
```


- `组合拳2`

```python
>>#contains函数+local-name函数定位节点名包含di的元素
>>print tree.xpath('//div[@id="testid"]/following::div[contains(local-name(),"di")]') 
>>[<Element div at 0x225e108>, <Element div at 0x225e0c8>]
```

- `or：多条件匹配`

```python
>>print tree.xpath('//li[@data="one" or @code="84"]/text()') #or匹配多个条件
>>['1', '84']
>>#也可使用|
>>print tree.xpath('//li[@data="one"]/text() | //li[@code="84"]/text()') #|匹配多个条件
>>['1', '84']
```

- `组合拳3：floor + div除法 + ceiling`
```python
>>#position定位+last+div除法，选取中间两个
>>tree.xpath('//div[@id="go"]/ul/li[position()=floor(last() div 2+0.5) or position()=ceiling(last() div 2+0.5)]/text()') 
>>['5', '6']
```

- `组合拳4隔行定位：position+mod取余`
```python
>>#position+取余运算隔行定位
>>tree.xpath('//div[@id="go"]/ul/li[position()=((position() mod 2)=0)]/text()') 
```

- `starts-with：以。。开始`
```python
>>#starts-with定位属性值以8开头的li元素
>>print tree.xpath('//li[starts-with(@code,"8")]/text()')[0]
>>84
```

#### 8、数值比较

- `<：小于`
```python
>>#所有li的code属性小于200的节点
>>print tree.xpath('//li[@code<200]/text()')
>>['84', '104']
```

- `div：对某两个节点的属性值做除法`
```python
>>print tree.xpath('//div[@id="testid"]/ul/li[3]/@code div //div[@id="testid"]/ul/li[1]/@code')
>>2.65476190476
```

- `组合拳4：根据节点下的某一节点数量定位`
```python
>>#选取所有ul下li节点数大于5的ul节点
>>print tree.xpath('//ul[count(li)>5]/li/text()')
>>['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
```

#### 9、将对象还原为字符串
```python
>>> s = tree.xpath('//*[@id="testid"]')[0] #使用xpath定位一个节点
>>> s
<Element div at 0x2b6ffc8>
>>> s2 = etree.tostring(s) #还原这个对象为html字符串
>>> s2
'<div id="testid">\n\t\t<h2>&#213;&#226;&#192;&#239;&#202;&#199;&#184;&#246;&#208;&#161;&#177;&#234;&#204;&#226;</h2>\n\t\t<ol>\n\t\t\t<li data="one">1</li>\n\t\t\t<li data="two">2</li>\n\t\t\t<li data="three">3</li>\n\t\t</ol>\n\t\t<ul>\n\t\t\t<li code="84">84</li>\n\t\t\t<li code="104">104</li>\n\t\t\t<li code="223">223</li>\n\t\t</ul>\n\t</div>\n\t'
```

#### 10、选取一个属性中的多个值
举例：`<div class="mp-city-list-container mp-privince-city" mp-role="provinceCityList">`  
选择这个div的方案网上有说用and的，但是似乎只能针对不同的属性的单个值  
本次使用contains
```python
>>.xpath('div[contains(@class,"mp-city-list-container mp-privince-city")]')
>>当然也可以直接选取其属性的第二个值
>>.xpath('div[contains(@class,"mp-privince-city")]')
>>重点是class需要添加一个@符号



**如果您觉得本文结对您有帮助,通过微信打赏作者,金额随意!**

![](https://github.com/ghostwwl/machine_learning/blob/master/wx_pay.jpg)
