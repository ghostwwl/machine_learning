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

