#!/usr/bin/python
#-*- coding:utf-8 -*- 

import time
import re
import os
import sys
import codecs
import string
import shutil
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt   

from pxmysql import ClassMySql


import jieba.posseg as pseg
import jieba
# 这里并行分词
#jieba.enable_parallel(4)


class Text_Tfidf_Kmeans(object):
    def __init__(self, num_of_clusters=3):
        self.dbhost = '192.168.3.127'
        self.dbuser = 'ghostwwl'
        self.dbpwd = '********'
        self.dbname = 'ghostwwl'
        self.db = ClassMySql(self.dbhost, self.dbuser, self.dbpwd, self.dbname, True)
        # 文本标签 一个文本用一个标签表示
        self.tag_list = []
        # 标本
        self._corpus = []
        self.TDIDF_WORDS = None
        self.TDIDF_WEIGHT = None
        # 分词后 按照词性类别过滤掉一些词 降低维度
        self.word_filter_type = (u'x', u'uj', u'c', u'e')
        self.word_filter_type = ()
        # 分词后 我们需要选取的词性 [假设我们这里只需要各种名词]
        self.word_select_type = (u'n', u'nr', u'ns', u'nt', u'nz', u'nw', u'an', u'vn')
        
        # kmeans 聚类中心数
        self.num_of_clusters = num_of_clusters
        
    # 载入标本
    def load_the_specimen(self):
        sql = "select * from ecs_art_member_profile where area='华东地区' limit 500"
        #sql = "select * from coin_info where dynasty like '%宋%' and note is not null limit 500"
        flag, result = self.db.execute(sql)
        if not flag:
            print result
        
        # 对每个标本做预处理
        for r in result:
            self.tag_list.append(r['name'])
            #tmp_text = "%s%s%s%s%s" % (r['name'] or '', r['address'] or '', r['artworktype'] or '', r['artkindtype'] or '',
                                       #r['bio'] or '')
            #tmp_text = "%s%s" % (r['name'] or '', r['bio'] or '')
            
            # 生成每个标本需要做文本处理的 text
            tmp_text = "%s%s" % (r['name'] or '', r['note'] or '')
            tmp_text = r['note'] or ''
            #tmp_text = r['bio'] or ''
            tmp_text = unicode(tmp_text, "utf-8", 'ignore')
            # 分词及词性标注
            content_words = pseg.cut(tmp_text)
            if content_words:
                #tws = map(lambda x: x.word.encode('utf-8', 'ignore'), filter(lambda y:y.flag not in self.word_filter_type and y.flag in self.word_select_type  and len(y.word)>1, content_words))
                tws = map(lambda x: x.word.encode('utf-8', 'ignore'), filter(lambda y:y.flag not in self.word_filter_type and len(y.word)>1, content_words))
                self._corpus.append(' '.join(tws))
        
        self.db.disconnect()
        
    

    def TDIDF(self):
        #self.load_the_specimen()
        self.load_the_specimen1()
        if not len(self._corpus):
            print '没有任何语料输入'
        else:
            vectorizer = CountVectorizer()
            transformer = TfidfTransformer()  
            tfidf = transformer.fit_transform(vectorizer.fit_transform(self._corpus)) 
            
            #获取词袋模型中的所有词语  
            self.TDIDF_WORDS = vectorizer.get_feature_names()  
            #将tf-idf矩阵抽取出来，元素w[m][n]表示n词在j标本中的tf-idf权重  
            self.TDIDF_WEIGHT = tfidf.toarray()  
            
            
            # 有多少维特征 调试降维效果
            print '*****标本: %d 维度: %d 矩阵规模:[%d][%d]' % (len(self.tag_list), len(self.TDIDF_WEIGHT[0]), len(self.tag_list), len(self.TDIDF_WEIGHT[0]))
            
            
            # 打印词库模型
            #for kk, vv in  vectorizer.vocabulary_.iteritems():
                #print "%s --> %s" % (kk, vv)
                
            #print vectorizer.vocabulary_.get(u"静物")

            #tfidfdict = {}

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本
            # 第二个for便利某一类文本下的词语权重
            #for i in xrange(len(self.TDIDF_WEIGHT)):
                #for j in xrange(len(self.TDIDF_WORDS)):
                    #getword = self.TDIDF_WORDS[j]
                    #getvalue = self.TDIDF_WEIGHT[i][j]
                    #if getvalue != 0:  #去掉值为0的项
                        #if tfidfdict.has_key(getword):  #更新全局TFIDF值
                            #tfidfdict[getword] += string.atof(getvalue)
                        #else:
                            #tfidfdict.update({getword:getvalue})
            #sorted_tfidf = sorted(tfidfdict.iteritems(), key=lambda d:d[1],  reverse = True )
            
            #for i in sorted_tfidf[:100]:
                #print i[0], " --> ", i[1]
            
    
    def do_kmeans(self):
        if self.num_of_clusters > len(self.TDIDF_WEIGHT):
            print "*******棒槌参数错了*******"
            return
        
        clf = KMeans(n_clusters=self.num_of_clusters, n_init=30)
        s = clf.fit(self.TDIDF_WEIGHT)  
        print s
        print self.TDIDF_WEIGHT
      
        #中心点 
        print '---------%d中心点------------' % self.num_of_clusters
        print clf.cluster_centers_
          
        #每个样本所属的簇  
        print '---------样本所属的簇------------'
        print clf.labels_
        
        #for i in xrange(len(clf.labels_)):
            #print i, clf.labels_[i]
      
        #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  
        print(clf.inertia_)
        
        
        # 结果展示呢
        result = {}
        keywords_result = {}
        for i in xrange(self.num_of_clusters):
            result[i] = []
            keywords_result[i] = {}

        for i in xrange(len(clf.labels_)):
            # i 表示标本序号
            result[clf.labels_[i]].append(self.tag_list[i])
            
            for j in xrange(len(self.TDIDF_WORDS)):
                word = self.TDIDF_WORDS[j]
                wwv = self.TDIDF_WEIGHT[i][j]
                if wwv != 0:
                    if keywords_result[clf.labels_[i]].has_key(word):
                        keywords_result[clf.labels_[i]][word] +=  string.atof(wwv)
                    else:
                        keywords_result[clf.labels_[i]].update({word:wwv})
                        
        
        sorted_results = sorted(result.iteritems(), key=lambda d:d[0],  reverse = False)
        for i in sorted_results:
            print "Label%d has items %d ] \n%s" % (i[0], len(i[1]) , ','.join(i[1]))
            sorted_words = sorted(keywords_result[i[0]].iteritems(), key=lambda d:d[1],  reverse = True)
            print "HOT:",
            for m in sorted_words[:10]:
                print m[0], '-->', m[1], ' | ',
            print "\n-----------------------------------\n"
            
            
    
if __name__ == "__main__":
    T = Text_Tfidf_Kmeans(5)
    T.TDIDF()
    T.do_kmeans()
    
