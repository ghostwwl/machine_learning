#!/usr/bin/python
#-*- coding: utf-8 -*-

#********************************
#   FileName: ltp.py
#   Author  : ghostwwl
#   Date    : 2017.2
#   Note    : 测试哈工大pyltp
#********************************


import os
import logging
import pyltp
from timeit import default_timer

logging.basicConfig(format='%(levelname)-8s %(asctime)s] %(message)s', level=logging.INFO)

#NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

#logging.basicConfig(level=logging.DEBUG,  
                    #format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    #datefmt='%a, %d %b %Y %H:%M:%S',  
                    #filename='/tmp/test.log',  
                    #filemode='w') 

class Ltp(object):
    def __init__(self):
        self.model_dir = '/data/ghostwwl/project/ltp_data'
        self.segmentor = None
        self.postagger = None
        self.recognizer = None
        self.parser = None
        self.labeller = None
        self.debug = True
        self.loger = logging.getLogger()
        if self.debug:
            self.loger.setLevel(logging.DEBUG)
        self.DP_LABEL = dpLabelExplanationData = {
            "SBV" : {'relType' : "主谓关系" , 'description' : "subject-verb" ,  'example' : "我送她一束花 (我 <-- 送)"} ,
            "VOB" : {'relType' : "动宾关系" , "description" : "直接宾语，verb-object" , "example" : "我送她一束花 (送 --> 花)"} ,
            "IOB" : {'relType' : "间宾关系" , "description" : "间接宾语，indirect-object" , "example" : "我送她一束花 (送 --> 她)"} ,
            "FOB" : {'relType' : "前置宾语" , 'description' : "前置宾语，fronting-object" , 'example' : "他什么书都读 (书 <-- 读)"} ,
            "DBL" : {'relType' : "兼语" , 'description' : "double" , "example" : "他请我吃饭 (请 --> 我)"  } ,
            "ATT" : {'relType' : "定中关系" , 'description' : "attribute" , 'example' : "红苹果 (红 <-- 苹果)" } ,
            "ADV" : {'relType' : "状中结构" , 'description' : "adverbial" , 'example' : "非常美丽 (非常 <-- 美丽)"} ,
            "CMP" : {'relType' : "动补结构" , 'description' : "complement" , 'example' : "做完了作业 (做 --> 完)" } ,
            "COO" : {'relType' : "并列关系" , 'description' : "coordinate" , 'example' : "大山和大海 (大山 --> 大海)" } ,
            "POB" : {'relType' : "介宾关系" , 'description' : "preposition-object" , 'example' : "在贸易区内 (在 --> 内)"} ,
            "LAD" : {'relType' : "左附加关系" , 'description' : "left adjunct" , 'example' : "大山和大海 (和 <-- 大海)" } ,
            "RAD" : {'relType' : "右附加关系" , 'description' : "right adjunct" , 'example' : "孩子们 (孩子 --> 们)"} ,
            "IS" : {'relType' : '独立结构' , 'description' : 'independent structure' , 'example' : "两个单句在结构上彼此独立"  } ,
            "HED" : {'relType' : "核心关系" , 'description' : "head" , 'example' : "指整个句子的核心" },
            "WP" : {'relType' : "标点", 'description' : "punctuation", 'example' : "。"}
        }
        self.SDP_LABEL = {
            "Agt" : {"relType" : "施事关系" ,"description" : "Agent" , "example" : "我送她一束花 (我 <-- 送)"} ,
            "Exp" : {"relType" : "当事关系" ,"description" : "Experiencer" ,"example" : "我跑得快 (跑 --> 我)" } ,
            "Aft" : {"relType" : "感事关系" , "description" : "Affection" ,"example" : "我思念家乡 (思念 --> 我)"} ,
            "Poss" : {"relType" : "领事关系" ,"description" : "Possessor" ,"example" : "他有一本好读 (他 <-- 有)"} ,
            "Pat" : {"relType" : "受事关系" ,"description" : "Patient" ,"example" : "他打了小明 (打 --> 小明)"} ,
            "Cont" : {"relType" : "客事关系" ,"description" : "Content" ,"example" : "他听到鞭炮声 (听 --> 鞭炮声)"} ,
            "Prod" : {"relType" : "成事关系" ,"description" : "Product" , "example" : "他写了本小说 (写 --> 小说)"} ,
            "Orig" : {"relType" : "源事关系" ,"description" : "Origin" ,"example" : "我军缴获敌人四辆坦克 (缴获 --> 坦克)" } ,
            "Datv" : {"relType" : "源事关系" ,"description" : "Dative" ,"example" : "他告诉我个秘密 ( 告诉 --> 我 )"} ,
            "Comp" : {"relType" : "比较角色" ,"description" : "Comitative" ,"example" : "他成绩比我好 (他 --> 我)"} ,
            "Belg" : {"relType" : "属事角色" ,"description" : "Belongings" ,"example" : "老赵有俩女儿 (老赵 <-- 有)"} ,
            "Clas" : {"relType" : "类事角色" ,"description" : "Classification" ,"example" : "他是中学生 (是 --> 中学生)"} ,
            "Accd" : {"relType" : "依据角色" ,"description" : "According" ,"example" : "本庭依法宣判 (依法 <-- 宣判)"} ,
            "Reas" : {"relType" : "缘故角色" , "description" : "Reason" ,"example" : "他在愁女儿婚事 (愁 --> 婚事)" } ,
            "Int" : {"relType" : "意图角色" ,"description" : "Intention" ,"example" : "为了金牌他拼命努力 (金牌 <-- 努力)"} ,
            "Cons" : {"relType" : "结局角色" ,"description" : "Consequence" ,"example" : "他跑了满头大汗 (跑 --> 满头大汗)"} ,
            "Mann" : {"relType" : "方式角色" ,"description" : "Manner" ,"example" : "球慢慢滚进空门 (慢慢 <-- 滚)"} ,
            "Tool" : {"relType" : "工具角色" ,"description" : "Tool" ,"example" : "她用砂锅熬粥 (砂锅 <-- 熬粥)"} ,
            "Malt" : {'relType' : "材料角色" ,"description" : "Material" ,"example" : "她用小米熬粥 (小米 <-- 熬粥)"} ,
            "Time" : {'relType' : "时间角色" ,"description" : "Time" ,"example" : "唐朝有个李白 (唐朝 <-- 有)"} ,
            "Loc" : {"relType" : "空间角色" ,"description" : "Location" ,"example" : "这房子朝南 (朝 --> 南)"} ,
            "Proc" : {"relType" : "历程角色" ,"description" : "Process" ,"example" : "火车正在过长江大桥 (过 --> 大桥)"} ,
            "Dir" : {"relType" : "趋向角色" ,"description" : "Direction" ,"example" : "部队奔向南方 (奔 --> 南)"} ,
            "Sco" : {"relType" : "范围角色" ,"description" : "Scope" ,"example" : "产品应该比质量 (比 --> 质量)"} ,
            "Quan" : {'relType' : "数量角色" ,"description" : "Quantity" ,"example" : "一年有365天 (有 --> 天)"} ,
            "Qp" : {'relType' : "数量数组" ,"description" : "Quantity-phrase" ,"example" : "三本书 (三 --> 本)"} ,
            "Freq" : {'relType' : "频率角色" ,"description" : "Frequency" ,"example" : "他每天看书 (每天 <-- 看)"} ,
            "Seq" : {'relType' : "顺序角色" ,'description' : "Sequence" ,"example" : "他跑第一 (跑 --> 第一)"} ,
            'Desc' : {'relType' : "描写角色" ,'description' : "Description" , 'example' : "他长得胖 (长 --> 胖)"} ,
            'Feat' : {'relType' : "描写角色" ,'description' : "Description" , 'example' : "他长得胖 (长 --> 胖)"} ,
            'Host' : {'relType' : "宿主角色" ,'description' : "Host" ,"example" : "住房面积 (住房 <-- 面积)"} ,
            "Nmod" : {'relType' : "名字修饰角色" ,"description" : "Name-modifier" ,"example" : "果戈里大街 (果戈里 <-- 大街)"} ,
            "Tmod" : {'relType' : "时间修饰角色" ,'description' : "Time-modifier" ,"example" : "星期一上午 (星期一 <-- 上午)"} ,
            "r + main role" : {'relType' : "反角色" ,"description" : "" ,"example" : "打篮球的小姑娘 (打篮球 <-- 姑娘)"} ,
            'd + main role' : {'relType' : "嵌套角色" ,'description' : "" ,"example" : "爷爷看见孙子在跑 (看见 --> 跑)" } ,
            "eCoo" :{'relType' : "并列关系" ,"description" : "event Coordination" ,'example' : "我喜欢唱歌和跳舞 (唱歌 --> 跳舞)"} ,
            "eSelt" : {'relType' : "选择关系" ,'description' : "event Selection" ,'example' : "您是喝茶还是喝咖啡 (茶 --> 咖啡)"} ,
            'eEqu' : {'relType' : "等同关系" ,"description" : "event Equivalent" ,"example" : "他们三个人一起走 (他们 --> 三个人)"} ,
            "ePrec" :{'relType' : "先行关系" ,'description' : "event Precedent" ,"example" : "首先，先"} ,
            'eSucc' : {'relType' : "顺承关系" ,"description" : "event Successor" ,"example" : "随后，然后"} ,
            "eProg" : {'relType' : "递进关系" ,'description' : "event Progression" ,'example' : "况且，并且" } ,
            'eAdvt' : {'relType' : "转折关系" ,'description' : "event adversative" ,'example' : "却，然而"} ,
            'eCau' : {'relType' : "原因关系" ,"description" : "event Cause" ,"example" : "因为，既然"} ,
            "eResu" : {'relType' : "结果关系" ,'description' : "event Result" ,'example' : "因此，以致"} ,
            "eInf" : {'relType' : "推论关系" ,'description' : "event Inference" ,'example' : "才，则"} ,
            "eCond" : {'relType' : "条件关系" ,'description' : "event Condition" ,'example' : "只要，除非"} ,
            "eSupp" : {'relType' : "假设关系" ,"description" : "event Supposition" ,"example" : "如果，要是"} ,
            "eConc" : {'relType' : "让步关系" ,"description" : "event Concession" ,"example" : "纵使，哪怕"} ,
            "eMetd" : {'relType' : "手段关系" ,"description" : "event Method" ,"example" : ""} ,
            "ePurp" : {'relType' : "目的关系" ,'description' : "event Purpose" ,"example" : "为了，以便"} ,
            'eAban' : {'relType' : "割舍关系" ,"description" : "event Abandonment" ,'example' : "与其，也不"} ,
            'ePref' : {'relType' : "选取关系" ,'description' : "event Preference" ,'example' : "不如，宁愿" } ,
            'eSum' : {'relType' : "总括关系" ,'description' : "event Summary" ,"example" : "总而言之"} ,
            'eRect' : {'relType' : "分叙关系" ,'description' : "event Recount" ,"example" : "例如，比方说"} ,
            'mConj' : {'relType' : "连词标记" ,'description' : "Recount Marker" ,"example" : "和，或"} , 
            "mAux" : {'relType' : "的字标记" ,"description" : "Auxiliary" ,"example" : "的，地，得"} ,
            "mPrep" : {'relType' : "介词标记" ,'description' : "Preposition" ,"example" : "把，被"} ,
            "mTone" : {"relType" : "语气标记" ,"description" : "Tone" , "example" : "吗，呢"} ,
            "mTime" : {'relType' : "时间标记" ,"description" : "Time" ,"example" : "才，曾经" } ,
            "mRang" : {'relType' : "范围标记" ,"description" : "Range" ,"example" : "都，到处"} ,
            "mDegr" : {'relType' : "程度标记" , 'description' : "Degree" ,"example" : "很，稍微"} ,
            "mFreq" : {'relType' : "频率标记" ,"description" : "Frequency Marker" ,"example" : "再，常常"} ,
            "mDir" : {'relType' : "趋向标记" ,"description" : "Direction Marker" ,"example" : "上去，下来"} ,
            "mPars" : {'relType' : "插入语标记" ,"description" : "Parenthesis Marker" ,"example" : "总的来说，众所周知"} ,
            "mNeg" : {'relType' : "否定标记" ,'description' : "Negation Marker" ,'example' : "不，没，未"} ,
            'mMod' : {'relType' : "情态标记" , 'description' : "Modal Marker" , "example" : "幸亏，会，能"} ,
            'mPunc' : {'relType' : "标点标记" , 'description' : "Punctuation Marker" ,'example' : "，。！"} ,
            "mPept" : {'relType' : "重复标记" ,'description' : "Repetition Marker" ,"example" : "走啊走 (走 --> 走)"} ,
            'mMaj' : {'relType' : "多数标记" ,'description' : "Majority Marker" ,"example" : "们，等"} ,
            'mVain' : {'relType' : '实词虚化标记' ,'description' : "Vain Marker" ,"example" : ""} ,
            "mSepa" : {'relType' : "离合标记" ,'description' : "Seperation Marker" ,'example' : "吃了个饭 (吃 --> 饭) 洗了个澡 (洗 --> 澡)"} ,
            'Root' : {'relType' : "根节点" , 'description' : "Root" , 'example' : "全句核心节点"}
        } 
        self.POS_LABEL = {
            'a' : {'description' : "adjective" ,'example' : "美丽"} ,
            'b' : {'description' : "other noun-modifier" ,'example' : "大型, 西式"}  ,
            'c' : {'description' : "conjunction" ,'example' : "和, 虽然"} ,
            'd' : {'description' : 'adverb' ,'example' : '很'} ,
            'e' : {'description' : 'exclamation' ,'example' : '哎'} ,
            'g' : {'description' : "morpheme" ,'example' : "茨, 甥"} ,
            'h' : {'description' : "prefix" ,'example' : "阿, 伪"} , 
            'i' : {'description' : 'idiom' ,'example' : '百花齐放'} ,
            'j' : {'description' : 'abbreviation' ,'example' : '公检法'} ,
            'k' : {'description' : "suffix" ,'example' : '界, 率'} ,
            'm' : {'description' : 'number' ,'example' : '一, 第一'} ,
            'n' : {'description' : 'general noun' ,'example' : "苹果"} ,
            'nd' : {'description' : "direction noun" ,'example' : "右侧"} ,
            'nh' : {'description' : 'person name' ,'example' : '杜甫, 汤姆'} ,
            'ni' : {'description' : "oranization name" ,'example' : '保险公司'} ,
            'nl' : {'description' : "location noun" ,'example' : '城郊'} ,
            'ns' : {'description' : 'geographical name' ,'example' : '北京'} ,
            'nt' : {'description' : 'temporal noun' ,'example' : '近日, 明代'} ,
            'nz' : {'description' : 'other proper noun' ,'example' : '诺贝尔奖'} ,
            'o' : {'description' : "onomatopoeia" ,'example' : '哗啦'} ,
            'p' : {'description' : 'preposition' ,'example' : '在, 把'} ,
            'q' : {'description' : 'quantity' ,'example' : "个"} ,
            'r' : {'description' : "pronoun" ,'example' : '我们'} ,
            'u' : {'description' : 'auxiliary' ,'example' : '的, 地'} ,
            'v' : {'description' : "verb" ,'example' : '跑, 学习'} ,
            'wp' : {'description' : 'punctuation' ,'example' : "，。！"} ,
            'ws' : {'description' : 'foreign words' ,'example' : "CPU"} ,
            'x' : {'description' : 'non-lexeme' ,'example' : '萄, 翱'}
        }
        self.SRL_LABEL = {
            "A0" : {'description' : "通常表示动作的施事"} ,
            "A1" : {'description' : "通常表示动作的影响等"} ,
            "A2" : {'description' : "根据谓语动词不同会有不同的语义含义"} ,
            "A3" : {'description' : "根据谓语动词不同会有不同的语义含义"} ,
            "A4" : {'description' : "根据谓语动词不同会有不同的语义含义"} ,
            "A5" : {'description' : "根据谓语动词不同会有不同的语义含义"} ,
            "ADV" : {"description" : "adverbial, default tag ( 附加的，默认标记 )"} ,
            "BNE" : {'description' : "beneﬁciary ( 受益人 )"} ,
            'CND' : {'description' : "condition ( 条件 )"} ,
            'DIR' : {'description' : "direction ( 方向 )"} ,
            "DGR" : {'description' : "degree ( 程度 )"} ,
            'EXT' : {'description' : "extent ( 扩展 )" } ,
            "FRQ" : {'description' : "frequency ( 频率 )"} ,
            "LOC" : {'description' : "locative ( 地点 )"} ,
            "MNR" : {'description' : "manner ( 方式 )"} ,
            "PRP" : {'description' : "purpose or reason ( 目的或原因 )"} ,
            "TMP" : {'description' : "temporal ( 时间 )"} ,
            "TPC" : {'description' : "topic ( 主题 )"} ,
            "CRD" : {'description' : "coordinated arguments ( 并列参数 )"} ,
            "PRD" : {'description' : "predicate ( 谓语动词 )"} ,
            "PSR" : {'description' : "possessor ( 持有者 )"} ,
            "PSE" : {'description' : "possessee ( 被持有 )" }
        }
        
    def __del__(self):
        for x in self.segmentor, self.postagger, self.parser, self.labeller:
            if x is not None:
                x.release()
            del x
            
    # 分句
    def do_split_sentence(self, intxt):
        sentences =  pyltp.SentenceSplitter.split(intxt)
        return list(sentences)
        
        
    # 分词
    def do_seg(self, intxt):
        if self.segmentor is None:
            self.segmentor = pyltp.Segmentor()
            if self.debug:
                load_start = default_timer()
            # 这里可以自定义词典的 外部词典本身是一个文本文件（plain text），每行指定一个词，编码同样须为 UTF-8    
            #self.segmentor.load_with_lexicon('模型地址, '用户字典') # 加载模型
            self.segmentor.load(os.path.join(self.model_dir, 'cws.model'))
            if self.debug:
                load_use = default_timer() - load_start
                self.loger.debug("load cws.model use [ %f ] s" % load_use)
            
        words = self.segmentor.segment(intxt)
        return list(words)
    
    
    # 词性标注
    def do_pos(self, intxt):
        words = self.do_seg(intxt)
        if self.postagger is None:
            self.postagger = pyltp.Postagger()
            if self.debug:
                load_start = default_timer()
            self.postagger.load(os.path.join(self.model_dir, 'pos.model'))
            if self.debug:
                load_use = default_timer() - load_start
                self.loger.debug("load pos.model use [ %f ] s" % load_use)
            
        postags = self.postagger.postag(words)
        
        return words, list(postags)
    
    # 命名实体识别
    def do_entity(self, words, postags):
        if self.recognizer is None:
            self.recognizer = pyltp.NamedEntityRecognizer()
            if self.debug:
                load_start = default_timer()
            self.recognizer.load(os.path.join(self.model_dir, 'ner.model'))
            if self.debug:
                load_use = default_timer() - load_start
                self.loger.debug("load ner.model use [ %f ] s" % load_use)
            
        netags = self.recognizer.recognize(words, postags)
        
        return list(netags)
    
    # 依存句法分析
    def do_parers(self, words, postags):
        if self.parser is None:
            self.parser = pyltp.Parser() 
            if self.debug:
                load_start = default_timer()
            self.parser.load(os.path.join(self.model_dir, 'parser.model'))
            if self.debug:
                load_use = default_timer() - load_start
                self.loger.debug("load parser.model use [ %f ] s" % load_use)
        
        arcs = self.parser.parse(words, postags)
        
        return arcs
        
    # 角色标注
    def do_rolelabel(self, words, postags, netags, arcs):
        if self.labeller is None:
            self.labeller = pyltp.SementicRoleLabeller()
            if self.debug:
                load_start = default_timer()
            self.labeller.load(os.path.join(self.model_dir,'srl'))
            if self.debug:
                load_use = default_timer() - load_start
                self.loger.debug("load srl model use [ %f ] s" % load_use)
            
        roles = self.labeller.label(words, postags, netags, arcs)
        
        return roles
    
    
 


if __name__ == '__main__':
    T = Ltp()
    
    #for i in T.do_split_sentence('''据英国《卫报》报道，谷歌日前遭到美国劳工部（DoL）起诉，因该公司向女性员工支付的薪酬常常低于男性员工。上周五由在一名联邦行政法法官主持的听证会上，美国劳工部指出，他们发现“几乎整个谷歌存在系统性薪酬不公问题”。美国劳工部从2015年起指出谷歌存在薪酬不公问题，并曾要求该公司公布其他记录来协助调查。'''):
        #print i
        #print '-'*20 
    
    intxt = ['元芳你怎么看？我就趴窗口上看呗！',
        '在很多人眼中我就是神!',
        '孩子们你要什么样的生活?',
        '对于识别器来说知道一个词的正确发音是非常重要的',
        '2007年5月1日是个好日子',
        '王辉, 中国美术家协会会员。1980年生于湖北。2003年毕业于湖北美术学院, 中国画专业, 获得学士学位。',
    ]
    
    for x in intxt:
        # 依存句法分析
        words, postags = T.do_pos(x)
        arcs = T.do_parers(words, postags)
        netags = T.do_entity(words, postags)
        roles = T.do_rolelabel(words, postags, netags, arcs)
        
        T.loger.info("intxt: %s" % x)
        T.loger.info(" ".join('%d:%s/%s[%d:%s]' % (x[0], x[1], x[2], x[3].head, x[3].relation) for x in zip(range(1, len(postags)+1), words, postags, arcs)))

        result = []
        for x in zip(xrange(1, len(postags)+1), words, postags, arcs):
            result.append({'inx':x[0], 'words':x[1], 'pos':x[2], 'parent':x[3].head, 'relation':x[3].relation})
        
        # 角色标注
        for role in roles:
            for arg in role.arguments:
                w = []
                for i in xrange(arg.range.start, arg.range.end + 1):
                    w.append(result[i]['words'])
                
                r = '%s(%d, %d): %s' % (arg.name, arg.range.start, arg.range.end, ' '.join(w))
                T.loger.info(r)
            
            print role.index, " ".join(['%s:(%d,%d)'%(arg.name, arg.range.start, arg.range.end) for arg in role.arguments])
        
        T.loger.info('-'*60)
        
        
        
        
