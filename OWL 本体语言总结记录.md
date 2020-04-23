# OWL 本体语言总结记录


## 基础

OWL 是一门供处理 web 信息的语言, 于 2004 年 2 月成为一项 W3C 的推荐标准

 - XML
    - 不知道这个你就不是好的 IT 工人
    - 弱弱的来句 `<![CDATA["不知cdata的肯定没处理过中文xml"]]>`
    - https://www.w3.org/XML/
 - RDF
    - Resource Description Framework
    - 资源描述框架，本质是一个数据模型（Data Model）, http://www.w3.org/RDF/
    - RDF形式为SPO三元组，也称为一条语句（statement），知识图谱中我们也称其为一条知识
        - Subject -- Predicate --> Object
    - RDF序列化
        - RDF/XML
            - 用XML的格式来表示RDF数据
            - 例:
                ```
                    <?xml version="1.0" encoding="UTF-8"?>
                    <rdf:RDF
                       xmlns:owl="http://www.w3.org/2002/07/owl#"
                       xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                       xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                    >
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/Style">
                        <rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">风格描述</rdfs:comment>
                        <rdfs:subClassOf rdf:resource="http://schema.jd.com/ontologies/Intangible"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Class"/>
                      </rdf:Description>
                      <rdf:Description rdf:nodeID="N72957783ad8543ecaf879f81de449f66">
                        <owl:onProperty rdf:resource="http://schema.jd.com/ontologies/is_concept"/>
                        <owl:someValuesFrom rdf:resource="http://schema.jd.com/ontologies/ConceptProduct"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Restriction"/>
                      </rdf:Description>
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/sku_used_by_object">
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#ObjectProperty"/>
                        <rdfs:domain rdf:resource="http://schema.jd.com/ontologies/SKU"/>
                        <rdfs:subPropertyOf rdf:resource="http://schema.jd.com/ontologies/sku_to_attribute"/>
                        <rdfs:range rdf:resource="http://schema.jd.com/ontologies/Thing"/>
                        <rdfs:comment>适用对象</rdfs:comment>
                      </rdf:Description>
                      <rdf:Description rdf:nodeID="Ne066a7e718464eaf996951c7a3055829">
                        <owl:onProperty rdf:resource="http://schema.jd.com/ontologies/is_accessory_product"/>
                        <owl:someValuesFrom rdf:resource="http://schema.jd.com/ontologies/Product"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Restriction"/>
                      </rdf:Description>
                      <rdf:Description rdf:nodeID="Nbac471e4192441b0be1bcf0e2fc73578">
                        <owl:onProperty rdf:resource="http://schema.jd.com/ontologies/sku_has_design"/>
                        <owl:someValuesFrom rdf:resource="http://schema.jd.com/ontologies/Design"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Restriction"/>
                      </rdf:Description>
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/Function">
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Class"/>
                        <rdfs:subClassOf rdf:resource="http://schema.jd.com/ontologies/Intangible"/>
                        <rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">产品的功能</rdfs:comment>
                      </rdf:Description>
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/IP">
                        <rdfs:comment>兴趣点。这是一个虚类，主要是标注上方便。并不能和某个特定实体类型建立父子关系。</rdfs:comment>
                        <rdfs:subClassOf rdf:resource="http://schema.jd.com/ontologies/Thing"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Class"/>
                        <rdfs:comment>Interested Point</rdfs:comment>
                      </rdf:Description>
                      <rdf:Description rdf:nodeID="N27dd61938f434ec0978691d2977a186d">
                        <owl:someValuesFrom rdf:resource="http://schema.jd.com/ontologies/Function"/>
                        <owl:onProperty rdf:resource="http://schema.jd.com/ontologies/entity_has_function"/>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Restriction"/>
                      </rdf:Description>
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/sku_used_in_scene">
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#ObjectProperty"/>
                        <rdfs:subPropertyOf rdf:resource="http://schema.jd.com/ontologies/sku_to_attribute"/>
                      </rdf:Description>
                      <rdf:Description rdf:about="http://schema.jd.com/ontologies/Unknown">
                        <rdfs:subClassOf rdf:resource="http://schema.jd.com/ontologies/Thing"/>
                        <rdfs:comment>未知词类型，这个表专门用于分析未召回类型的词</rdfs:comment>
                        <rdf:type rdf:resource="http://www.w3.org/2002/07/owl#Class"/>
                      </rdf:Description>
                ```
        - N-Triples
            - 多个三元组来表示RDF数据集
            - https://www.w3.org/TR/2014/REC-n-triples-20140225/
        - Turtle
            - 较多使用RDF序列化方式， 比RDF/XML紧凑， 比N-Triples可读性好
                ```text
                @prefix : <http://schema.jd.com/ontologies/> .
                @prefix owl: <http://www.w3.org/2002/07/owl#> .
                @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
                @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
                @prefix xml: <http://www.w3.org/XML/1998/namespace> .
                @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
                
                : a owl:Ontology .
                
                :Action a owl:Class ;
                    rdfs:subClassOf :Thing .
                
                :Actor a owl:Class ;
                    rdfs:subClassOf :EntertainmentPerson .
                
                :AnimalAudience a owl:Class ;
                    rdfs:comment "动物受众。如：猫、狗、鹦鹉等"^^xsd:string ;
                    rdfs:subClassOf :Audience .
                
                :AthleticPerson a owl:Class ;
                    rdfs:comment "体育人物" ;
                    rdfs:subClassOf :Person .
                
                :BodyAudience a owl:Class ;
                    rdfs:comment "用于描述身体部位"^^xsd:string ;
                    rdfs:subClassOf :Audience .
                
                :Book a owl:Class ;
                    rdfs:comment "书籍"^^xsd:string ;
                    rdfs:subClassOf :CreativeWork .
                
                :BrandColor a owl:Class ;
                    rdfs:comment "手机颜色。如：有些特殊词汇，是手机厂商发明的"^^xsd:string ;
                    rdfs:subClassOf :Color .
                
                :City a owl:Class ;
                    rdfs:comment "城市" ;
                    rdfs:subClassOf :AdministrativeArea .
                
                :ClothesProduct a owl:Class ;
                    rdfs:subClassOf :ProductCategory .
                
                ```
        - RDFa
            - The Resource Description Framework in Attributes
            - HTML5的一个扩展，在不改变任何显示效果的情况下，让网站构建者能够在页面中标记实体，像人物、地点、时间、评论等
            - 目的是，将RDF数据嵌入到网页中，使搜索引擎能够更好的解析非结构化页面，从而有用的结构化信息
        - JSON-LD
            - JSON for Linking Data, 用键值对的方式来存储RDF数据
            - 例:
                ```json 
                [
                  {
                    "@id": "http://schema.jd.com/ontologies/SceneSport",
                    "@type": [
                      "http://www.w3.org/2002/07/owl#Class"
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#comment": [
                      {
                        "@value": "运动"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                      {
                        "@id": "http://schema.jd.com/ontologies/Scenes"
                      }
                    ]
                  },
                  {
                    "@id": "http://schema.jd.com/ontologies/Style",
                    "@type": [
                      "http://www.w3.org/2002/07/owl#Class"
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#comment": [
                      {
                        "@value": "风格描述"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                      {
                        "@id": "http://schema.jd.com/ontologies/Intangible"
                      }
                    ]
                  },
                  {
                    "@id": "http://schema.jd.com/ontologies/sku_used_by_event",
                    "@type": [
                      "http://www.w3.org/2002/07/owl#ObjectProperty"
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#comment": [
                      {
                        "@value": "适用事件"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#domain": [
                      {
                        "@id": "http://schema.jd.com/ontologies/SKU"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#range": [
                      {
                        "@id": "http://schema.jd.com/ontologies/Event"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#subPropertyOf": [
                      {
                        "@id": "http://schema.jd.com/ontologies/sku_to_attribute"
                      }
                    ]
                  },
                  {
                    "@id": "http://schema.jd.com/ontologies/Movie",
                    "@type": [
                      "http://www.w3.org/2002/07/owl#Class"
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#comment": [
                      {
                        "@value": "电影"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                      {
                        "@id": "http://schema.jd.com/ontologies/CreativeWork"
                      }
                    ]
                  },
                  {
                    "@id": "http://schema.jd.com/ontologies/FictionalCharacter",
                    "@type": [
                      "http://www.w3.org/2002/07/owl#Class"
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#comment": [
                      {
                        "@value": "虚拟角色。来自创作品。理想情况下，每个FictionCharacter都应该与至少一个CreativeWork关联。"
                      }
                    ],
                    "http://www.w3.org/2000/01/rdf-schema#subClassOf": [
                      {
                        "@id": "http://schema.jd.com/ontologies/Thing"
                      }
                    ]
                  },
                  ]
                ```
        - 现在可能还有 csv 撒的 只要能表示三元组就行呵
 - RDFS
    - Resource Description Framework Schema
    - 轻量级的模式语言
    - RDFS/OWL序列化方式和RDF一样，其表现形式上，它们就是RDF
    - https://www.w3.org/TR/rdf-schema/
    - https://www.runoob.com/rdf/rdf-reference.html
 - OWL / OWL2
 
 
## 什么是 OWL？
- OWL 指的是 web 本体语言
- OWL 构建在 RDF 的顶端之上
- OWL 用于处理 web 上的信息
- OWL 被设计为供计算机进行解释
- OWL 不是被设计为供人类进行阅读的
- OWL 由 XML 来编写
- OWL 拥有三种子语言
    - OWL Lite
    - OWL DL (包含 OWL Lite)
    - OWL Full (包含 OWL DL)
- OWL 是一项 web 标准
    - https://www.w3.org/OWL/
    - https://www.w3.org/TR/owl-ref/


## OWL 基本知识

### 一、类和个体


### 资源相关关键字
- rdf:ID
    - 定义一个资源，或者说引入一个新的资源名称
- rdf:about
    - 可用来定义资源外（引入一个新的资源名称），
    - 还可用来扩展对这个资源的定义(这可以出现在其他本体文件中)
    - 例: 如果Pizza是用rdf:ID定义的，那么要增加对Pizza的描述，就必须用rdf:about, 因为同一个RDF文档中，不能出现两个rdf:ID="Pizza"
- rdf:resource
    - 用于属性对一个对象的引用
    - 可以是在前面或后面定义过的；也可以使引用未定义的，那样就会生成blank node


#### 具名类
- owl:Thing
    - OWL中的所有个体都是类owl:Thing的成员
- owl:Class
    - 用户自定义的类都隐含地是 owl:Thing的一个子类
- rdfs:subClassOf
    - 用于描述该类的父类
    
    
    
#### 匿名类

在一个明确的上下文 owl:Restriction 中限制属性的值域，
owl:onProperty 元素指出了受限制的属性。


1. 值约束
    - 定义一个类，其所有个体均满足：指定属性的全部取值均是指定类的个体（或指定值域的数值）
        - owl:Restriction+ 
            - owl:onProperty+ 
            - owl:allValuesFrom       
    - 定义一个类，其所有个体均满足：指定属性至少一个取值是指定类的个体（或指定值域的数值）
        - owl:Restriction+ 
            - owl:onProperty+ 
            - owl:someValuesFrom
    - 定义一个类，其所有个体均满足：指定属性有一个取值是指定类的个体（或指定值域的数值）
        - owl:Restriction+ 
            - owl:onProperty+ 
            - owl:hasValue
            

2. 基数约束
    - 定义一个类，其所有个体均满足：指定属性至多N（非负整数）个不同的取值（个体或数值）
        - owl:Restriction+ 
            - owl:onProperty+ 
            - owl:maxCardinality
    - 定义一个类，其所有个体均满足：指定属性至少N（非负整数）个不同的取值（个体或数值）
        - owl:Restriction+
            - owl:onProperty+
            - owl:minCardinality
    - 定义一个类，其所有个体均满足：指定属性正好N（非负整数）个不同的取值（个体或数值）
        - owl:Restriction+
            - owl:onProperty+
            - owl:Cardinality
            

#### 空类
- owl:Nothing
    - 定义空类


### 二、属性

属性是一个二元关系, 有两种类型的属性：

#### 属性关键字：

属性是一个二元关系

- owl:ObjectProperty
    - 对象属性（object properties）
    - 两个类的实例间的关系
- owl:DatatypeProperty
    - 数据类型属性（datatype properties）
    - 类实例与RDF文字或XML Schema数据类型间的关系
- rdfs:subPropertyOf
    - 包含关系 用于描述该属性的父属性
- rdfs:domain
    - 定义域 用于表示该属性属于哪个类别
- rdfs:range
    - 值域 用于描述该属性的取值类型



#### 属性特性：
1. owl:TransitiveProperty 传递属性
    > 如果一个属性P被声明为传递属性，那么对于任意的x,y和z： P(x,y)与P(y,z) 蕴含 P(x,z)；
    - 定义某属性具有传递性质
    - 例:  x <:isPartOf> y  and y <:isPartOf> z  那么 x <:isPartOf> z
2. owl:SymmetricProperty
    > 如果一个属性P被声明为对称属性，那么对于任意的x和y： P(x,y)当且仅当P(y,x)
    - 对称属性，描述定义某属性具有对称性
    - 例: 如果 A 和 B 对称，若 A 认识 B，那么B肯定认识A
3. owl:FunctionalProperty  
    > 如果一个属性P被标记为函数型属性，那么对于所有的x  , y, 和z:  P(x,y)与P(x,z) 蕴含 y = z
    - 函数型属性，描述属性取值的唯一性
    - 例: 定义人的 "父亲" 是唯一性的属性，如果 A 的父亲是 B，在另一个信息利存在 A 的父亲是 C，我们就可以得出 B == C
4. owl:inverseOf 逆属性：
    > 如果一个属性P1被标记为属性P2的逆, 那么对于所有的x 和 y:  P1(x,y) 当且仅当P2(y,x)。请注意owl:inverseOf的语法，它仅仅使用一个属性名作为参数。A 当且仅当B意思是 (A蕴含B)并且(B蕴含A).
    - 定义某属性的相反关系
    - 例: 定义 `父母` 的反关系是 `子女`， 那么 如果 A 是 B 的 `父母` 可以得出 B 是 A 的 `子女`
5. owl:InverseFunctionalProperty－－反函数属性：
    > 如果一个属性P被标记为反函数型的，那么对于所有的x, y和z:  P(y,x)与P(z,x) 蕴含 y = z。因为一个函数型属性的逆必定是反函数型的。反函数型属性的值域中的元素可以看成是在数据库意义上定义的一个唯一的键值。owl:InverseFunctional意味着属性的值域中的元素为定义域中的每个元素提供了一个唯一的标识。


### OWL使用XML Schema内嵌数据类型中的大部分 

- 下列数据类型是推荐在OWL中使用
    - xsd:string
    - xsd:normalizedString
    - xsd:boolean
    - xsd:decimal
    - xsd:float
    - xsd:double
    - xsd:integer
    - xsd:nonNegativeInteger
    - xsd:positiveInteger
    - xsd:nonPositiveInteger
    - xsd:negativeInteger
    - xsd:long
    - xsd:int
    - xsd:short
    - xsd:byte
    - xsd:unsignedLong
    - xsd:unsignedInt
    - xsd:unsignedShort
    - xsd:unsignedByte
    - xsd:hexBinary
    - xsd:base64Binary
    - xsd:dateTime
    - xsd:time
    - xsd:date
    - xsd:gYearMonth
    - xsd:gYear
    - xsd:gMonthDay
    - xsd:gDay
    - xsd:gMonth
    - xsd:anyURI
    - xsd:token
    - xsd:language
    - xsd:NMTOKEN
    - xsd:Name
    - xsd:NCName




### 三、属性限制

在一个明确的上下文 OWL：Restriction 中限制属性的值域，
owl：onProperty 元素指出了受限制的属性。
   
1. allValuesFrom, someValuesFrom
    - owl:allValuesFrom属性限制要求：
        > 对于每一个有指定属性实例的类实例，该属性的值必须是由 owl:allValuesFrom从句指定的类的成员。
    - owl:someValuesFrom限制与`owl:allValuesFrom`相似。
        > 这两种限制形式间的不同就是全称量词与存在量词间的不同。
     
2. 基数限制
    - owl:cardinality，这一约束允许对一个关系中的元素数目作出精确的限制。
    - owl:maxCardinality能够用来指定一个上界。
    - owl:minCardinality能够用来指定一个下界。
    > 使用`owl:maxCardinality` 和 `owl:minCardinality` 的组合就能够将一个属性的基数限制为一个数值区间。
      
3. hasValue [OWL DL]  
     hasValue 使得我们能够根据“特定的”属性值的存在来标识类。
     因此，一个个体只要至少有“一个”属性值等于hasValue的资源，这一个体就是该类的成员。

### 四、本体映射
   
为了让本体发挥最大的作用，就需要让本体得到充分的共享，为了使得在开发本体时尽可能的节省人力，就需要使得开发出来的本体能够被重要。
更理想的情况是他们能够被组合使用。在开发一个本体的过程中，很多精力都被投入到将类与属性联系起来以获取最大意义的工作上去了，意识到这一点是很重要的。
我们希望对类成员作出的断言较为简单同时又要有广泛的和有用的含意在里面。这也是在本体开发过程中最为困难的工作。
如果你能找到已经经过广泛使用和精炼的本体，那么采用它才有意义。

- owl:equivalentClass
    - 属性`owl:equivalentClass`被用来表示两个类有着完全相同的实例。但我们要注意，在OWL DL中，类仅仅代表着个体的集合而不是个体本身。
    - 在OWL FULL中，我们能够使用owl:sameAs来表示两个类在各方面均完全一致
- owl:equivalentProperty
    - 表示某个属性和另一个属性是相同的
    - 然而在OWL FULL中，我们能够使用owl:sameAs来表示两个类在各方面均完全一致。类似的，owl:equivalentProperty属性声明表达属性的等同
- owl:sameAs
    - 表示两个实体是同一个实体
    - 两个类用sameAs还是用equivalentClass效果是不同的
        - 用sameAs的时候，把一个类解释为一个个体，就像在OWL Full中一样，这有利于对本体进行分类
- owl:differentFrom
    - 不同的个体－－differentFrom, AllDifferent 
    - 这一机制提供了与sameAs相反

### 五、复杂类

1. 集合运算符
    - 交运算：intersectionOf
    - 并运算：unionOf
    - 补运算：complementOf
    
2. 枚举类 oneOf 
    - OWL提供了一种通过直接枚举类的成员的方法来描述类。这是通过使用oneOf结构来完成。特别地，这个定义完整地描述了类的外延，因此任何其他个体都不能被声明为属于这个类。oneOf结构的每一个元素都必须是一个有效声明的个体。一个个体必须属于某个类。

3. 不相交类 disjointWith
    - 使用owl:disjointWith构造子可以表达一组类是不相交的。它保证了属于某一个类的个体不能同时又是另一个指定类的实例。

### 六、本体的版本控制

- owl:Ontology
    - 元素内可以连接到 以前定义的本体版本
    
- owl:priorVersion
    - 用 rdf:resource 属性标识的参数 连接到以前的版本
    
- owl:imports
    - 提供了一种嵌入机制
    - 接受一个用 rdf:resource 属性标识的参数
    
- owl:backwardCompatibleWith
    - 兼容以前的版本
    
- owl:incompatibleWith
    - 不兼容以前的版本
    
- owl:DeprecatedClass
    - owl:DeprecatedClass 是 rdfs：Class 的子类
    - 表示这个类在将会在后续的版本中弃用

- owl:DeprecatedProperty
    - owl:DeprecatedProperty 是 rdf：Property 的子类
    - 表示这个属性将会在后续版本中弃用

    ```text
    # 我用 google 表示很好用
    # https://www.w3.org/TR/owl-ref/#Deprecation 的 google 翻译
    
    
    弃用是版本控制软件中常用的功能（例如，请参阅Java编程语言），
    它表示保留特定功能是为了向后兼容，但将来可能会淘汰。
    在这里，特定的标识符被称为 owl：DeprecatedClass 或 owl：DeprecatedProperty 类型，
    其中 owl：DeprecatedClass 是rdfs：Class的子类，
    而 owl：DeprecatedProperty是rdf：Property的子类。
    通过弃用术语，意味着该术语不应在用于本体的新文档中使用。
    这使得本体可以在逐步淘汰旧词汇的同时保持向后兼容性（因此，仅将弃用与向后兼容性结合使用才有意义）。
    结果，较容易将旧数据和应用程序迁移到新版本，从而可以提高对新版本的采用程度。
    除了RDF（S）模型理论给出的含义外，这在模型理论语义中没有任何意义。
    但是，当检查OWL标记时，创作工具可能会使用它来警告用户。
    
    ```

```

<owl:Ontology rdf:about=""> 
   <rdfs:comment>An example OWL ontology</rdfs:comment>
   <owl:priorVersion rdf:resource="http://www.w3.org/TR/2003/PR-owl-guide-20031215/wine"/> 
   <owl:imports rdf:resource="http://www.w3.org/TR/2004/REC-owl-guide-20040210/food"/> 
   <rdfs:label>Wine Ontology</rdfs:label> 
   
-------------------------- 我是分割线 -------------------------- 

<owl:Ontology rdf:about="">
  <rdfs:comment>Vehicle Ontology, v. 1.1</rdfs:comment>
  <owl:backwardCompatibleWith
          rdf:resource="http://www.example.org/vehicle-1.0"/>   
  <owl:priorVersion rdf:resource="http://www.example.org/vehicle-1.0"/>
</owl:Ontology>

<owl:DeprecatedClass rdf:ID="Car">
  <rdfs:comment>Automobile is now preferred</rdfs:comment>
  <owl:equivalentClass rdf:resource="#Automobile"/>
  <!-- note that equivalentClass only means that the classes have the same
       extension, so this DOES NOT lead to the entailment that
       Automobile is of type DeprecatedClass too -->        
</owl:DeprecatedClass>

<owl:Class rdf:ID="Automobile" />

<owl:DeprecatedProperty rdf:ID="hasDriver">
  <rdfs:comment>inverse property drives is now preferred</rdfs:comment>
  <owl:inverseOf rdf:resource="#drives" />
</owl:DeprecatedProperty>

<owl:ObjectProperty rdf:ID="drives" />

```
