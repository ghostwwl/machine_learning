#!/usr/bin/python
# -*- coding: utf-8 -*-

# ********************************
#     FileName : corpus_tfidf.py
#     Author   : ghostwwl
#     Date     : 2018/01/10
#     Note     :
# ********************************


__author__ = 'ghostwwl'

import re
import numpy as np
import joblib
import requests, ujson
from nltk import FreqDist
from urllib.parse import quote
from prettytable import PrettyTable
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

import sys, os
print(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .base import BaseObject

# 在包含 N 个文档的语料库中，随机选择一个文档。该文件总共包含 T 个词，词条「数据」出现 K 次。如果词条「数据」出现在文件总数的数量接近三分之一，
# 则 TF（词频）和 IDF（逆文档频率）的乘积的正确值是多少？
#
#
# K * Log(3) / T
#
#
#
# TF 的公式是 K/T
#
# IDF 的公式是 log
# = log(1 / (⅓))
# = log (3)
#
# 因此正确答案是 Klog(3)/T
#
#
#     word_total
# -------------------  X  log（1/(word_doc/all_doc))
# corpus_words_count



# '''
# # bigram 的 2-gram
#
# bigram_vectorizer = CountVectorizer(ngram_range=(1, 2),
#                                      token_pattern=r'\b\w+\b', min_df=1)
# analyze = bigram_vectorizer.build_analyzer()
# analyze('Bi-grams are cool!') == (
#      ['bi', 'grams', 'are', 'cool', 'bi grams', 'grams are', 'are cool'])
# True
# 因此，由这个向量器抽取的词表非常大，现在可以解决由于局部位置模型编码的歧义问题：
#
# X_2 = bigram_vectorizer.fit_transform(corpus).toarray()
#
# '''



def do_pos(intxt):
    u1 = 'http://cwsseg-cwsseg.cwsseg.xxxxxsvc.xht1.n.jd.local/pcut?i={0}'
    x2 = requests.get(u1.format(quote(intxt)))
    return ujson.decode(x2.content.decode('utf-8', 'ignore'))



class TfidfVec(BaseObject):
    def __init__(self):
        super(TfidfVec, self).__init__()
        # 文本标签 一个文本用一个标签表示
        self.tag_list = []
        # 文档标本
        self._corpus = []
        self.TDIDF_WORDS = None
        self.TDIDF_WEIGHT = None
        # 分词后 按照词性类别过滤掉一些词 降低维度
        self.word_filter_type = ('wp', 'm', 'ws', 'nt', 'v', 'e', 'a', 'k', 'o', 'r', 'u', 'ns', 'q', 'nh')
        # self.word_filter_type = ()
        # 分词后 我们需要选取的词性 [假设我们这里只需要各种名词]
        self._featurizer = None

    def reset(self):
        del self._corpus[:]
        del self.tag_list[:]
        self.TFIDF_WEIGHT = None
        self.TDIDF_WORDS = None
        return True

    def dump(self, model_file):
        joblib.dump(self._featurizer, model_file)

    def load(self, model_file):
        self._featurizer = joblib.load(model_file)

    def load_the_specimen(self, indocuments):
        # 对每个标本做预处理
        # 去掉里面的 数字 英文 空格 中划线 以及竖线
        reobj = re.compile('(?is)[a-z0-9A-Z\-/ \|]*')
        for docinx in range(len(indocuments)):
            document = indocuments[docinx]
            self.tag_list.append('document_%d' % docinx)

            # 生成每个标本需要做文本处理的 text
            in_text = document or ''
            in_text = reobj.sub('', in_text)
            # 分词及词性标注
            content_words = do_pos(in_text)
            if content_words:
                tws = map(lambda x: "{0}".format(x['word'], x['pos']),
                          filter(lambda y: y['pos'] not in self.word_filter_type and len(y['word'].decode('utf-8')) > 1,
                                 content_words)
                          )
                self._corpus.append(' '.join(tws))
        # del seg_engine

    def do_fit(self, indocuments, word_length = None, return_tfidf_words_info = False):
        '''
        使用此函数 fit 后 self._featurizer 为 TfidfVectorizer featurizer
        :param indocuments:
        :param word_length:
        :param return_tfidf_words_info:
        :return:
        '''
        if len(self._corpus) == 0 and len(indocuments) > 0:
            self.load_the_specimen(indocuments)

        if not len(self._corpus):
            print('没有任何语料输入')
            return None

        self._featurizer = TfidfVectorizer(norm=None)
        # binary：默认为False，tf-idf中每个词的权值是tf*idf，如果binary设为True，所有出现的词的tf将置为1，TfidfVectorizer计算得到的tf与CountVectorizer得到的tf是一样的，就是词频，不是词频/该词所在文档的总词数。
        # norm：默认为'l2'，可设为'l1'或None，计算得到tf-idf值后，如果norm='l2'，则整行权值将归一化，即整行权值向量为单位向量，如果norm=None，则不会进行归一化。大多数情况下，使用归一化是有必要的。
        # use_idf：默认为True，权值是tf*idf，如果设为False，将不使用idf，就是只使用tf，相当于CountVectorizer了。
        # smooth_idf：idf平滑参数，默认为True，idf=ln((文档总数+1)/(包含该词的文档数+1))+1，如果设为False，idf=ln(文档总数/包含该词的文档数)+1
        # sublinear_tf：默认为False，如果设为True，则替换tf为1 + log(tf)。

        tfidf = self._featurizer.fit_transform(self._corpus)
        self.TFIDF_WORDS = self._featurizer.get_feature_names()
        self.TFIDF_WEIGHT = tfidf.toarray()

        # 下面是调试信息
        total_word_idf = dict(zip(self.TFIDF_WORDS, self.TFIDF_WEIGHT.sum(0).tolist())).items()
        total_word_idf.sort(key=lambda x: x[1], reverse=True)

        if word_length > 0:
            total_word_idf = filter(lambda x: len(x[0].decode('utf-8', 'ignore')) >= word_length, total_word_idf)

        if not return_tfidf_words_info:
            table = PrettyTable()
            table.field_names = ["Words", "TF-IDF"]
            for word, tf in total_word_idf:
                table.add_row((word, tf))
            table.sortby = "TF-IDF"
            table.align = 'l'
            table.reversesort = True
            print(table)
        else:
            return total_word_idf

    def get_vec(self, documents):
        return self._featurizer.transform(documents).toarray()

#----------------------------------------------------------------------------------------
class DocVec(BaseObject):
    def __init__(self):
        super(CorpusTfidf, self).__init__()
        # 文本标签 一个文本用一个标签表示
        self.tag_list = []
        # 文档标本
        self._corpus = []
        self.TDIDF_WORDS = None
        self.TDIDF_WEIGHT = None
        # 分词后 按照词性类别过滤掉一些词 降低维度
        self.word_filter_type = ('wp', 'm', 'ws', 'nt', 'v', 'e', 'a', 'k', 'o', 'r', 'u', 'ns', 'q', 'nh')
        # self.word_filter_type = ()
        # 分词后 我们需要选取的词性 [假设我们这里只需要各种名词]
        self._featurizer = None

    def reset(self):
        del self._corpus[:]
        del self.tag_list[:]
        self.TFIDF_WEIGHT = None
        self.TDIDF_WORDS = None
        return True

    def load_the_specimen(self, indocuments):
        # 对每个标本做预处理
        # 去掉里面的 数字 英文 空格 中划线 以及竖线
        reobj = re.compile('(?is)[a-z0-9A-Z\-/ \|]*')
        for docinx in range(len(indocuments)):
            document = indocuments[docinx]
            self.tag_list.append('document_%d' % docinx)

            # 生成每个标本需要做文本处理的 text
            in_text = document or ''
            in_text = reobj.sub('', in_text)
            # 分词及词性标注
            content_words = do_pos(in_text)
            if content_words:
                if globals().has_key('_PRODUCT_SET'):
                    content_words = filter(lambda x: x['word'] in globals()['_PRODUCT_SET'], content_words)
                    pass
                tws = map(lambda x: "{0}".format(x['word'], x['pos']),
                          filter(lambda y: y['pos'] not in self.word_filter_type and len(y['word'].decode('utf-8')) > 1,
                                 content_words)
                          )
                self._corpus.append(TaggedDocument(tws, docinx))
        # del seg_engine

    def do_fit(self, indocuments, word_length = None):
        if len(self._corpus) == 0 and len(indocuments) > 0:
            self.load_the_specimen(indocuments)

        if not len(self._corpus):
            print('没有任何语料输入')
            return None

        self.logger.info('Start To Training Doc2Vec Model...')
        self._featurizer = Doc2Vec(self._corpus, vector_size=2000, epochs=20, workers=3)
        self.logger.info('Doc2Vec model Trained...')

        # debug
        for i in range(len(indocuments)):
            print('doc {0} feature: {1}'.format(i, self._featurizer.docvecs[i]))

    def get_vec(self, documents):

        return np.asarray( [self._featurizer.infer_vector(x.words) for x in documents])

        # return self._featurizer.transform(documents).toarray()


# ----------------------------------------------------------------------------------------
class CorpusTfidf(BaseObject):
    def __init__(self):
        super(CorpusTfidf, self).__init__()
        # 文本标签 一个文本用一个标签表示
        self.tag_list = []
        # 文档标本
        self._corpus = []
        self.TDIDF_WORDS = None
        self.TDIDF_WEIGHT = None
        # 分词后 按照词性类别过滤掉一些词 降低维度
        self.word_filter_type = ('wp', 'm', 'ws', 'nt', 'v', 'e', 'a', 'k', 'o', 'r', 'u', 'ns', 'q', 'nh')
        # self.word_filter_type = ()
        # 分词后 我们需要选取的词性 [假设我们这里只需要各种名词]
        self._featurizer = None

    def reset(self):
        del self._corpus[:]
        del self.tag_list[:]
        self.TFIDF_WEIGHT = None
        self.TDIDF_WORDS = None
        return True

    def get_vec(self, documents):
        return self._featurizer.transform(documents).toarray()

    def seve_mode(self, modelfile):
        return joblib.dump(self._featurizer, modelfile)

    def load_the_specimen(self, indocuments):
        # if 'seg_engine' not in  globals():
        #     seg_engine = LtpSegment()
        #     globals()['seg_engine'] = seg_engine
        # else:
        #     seg_engine = globals()['seg_engine']

        # 对每个标本做预处理
        # 去掉里面的 数字 英文 空格 中划线 以及竖线
        reobj = re.compile('(?is)[a-z0-9A-Z\-/ \|]*')
        for docinx in range(len(indocuments)):
            document = indocuments[docinx]
            self.tag_list.append('document_%d' % docinx)

            # 生成每个标本需要做文本处理的 text
            in_text = document or ''
            in_text = reobj.sub('', in_text)
            # 分词及词性标注
            # content_words = seg_engine.do_posword(in_text)
            content_words = do_pos(in_text)
            if content_words:
                if globals().has_key('_PRODUCT_SET'):
                    content_words = filter(lambda x: x['word'] in globals()['_PRODUCT_SET'], content_words)
                    pass
                tws = map(lambda x: "{0}".format(x['word'], x['pos']),
                          filter(lambda y: y['pos'] not in self.word_filter_type and len(y['word'].decode('utf-8')) > 1,
                                 content_words)
                          )
                self._corpus.append(' '.join(tws))
        # del seg_engine

    def do_tfidf2(self, indocuments, word_length = None, return_tfidf_words_info = False):
        '''
        使用此函数 fit 后 self._featurizer 为 TfidfVectorizer featurizer
        :param indocuments:
        :param word_length:
        :param return_tfidf_words_info:
        :return:
        '''
        if len(self._corpus) == 0 and len(indocuments) > 0:
            self.load_the_specimen(indocuments)

        if not len(self._corpus):
            print('没有任何语料输入')
            return None

        self._featurizer = TfidfVectorizer(norm=None)
        # binary：默认为False，tf-idf中每个词的权值是tf*idf，如果binary设为True，所有出现的词的tf将置为1，TfidfVectorizer计算得到的tf与CountVectorizer得到的tf是一样的，就是词频，不是词频/该词所在文档的总词数。
        # norm：默认为'l2'，可设为'l1'或None，计算得到tf-idf值后，如果norm='l2'，则整行权值将归一化，即整行权值向量为单位向量，如果norm=None，则不会进行归一化。大多数情况下，使用归一化是有必要的。
        # use_idf：默认为True，权值是tf*idf，如果设为False，将不使用idf，就是只使用tf，相当于CountVectorizer了。
        # smooth_idf：idf平滑参数，默认为True，idf=ln((文档总数+1)/(包含该词的文档数+1))+1，如果设为False，idf=ln(文档总数/包含该词的文档数)+1
        # sublinear_tf：默认为False，如果设为True，则替换tf为1 + log(tf)。

        tfidf = self._featurizer.fit_transform(self._corpus)
        self.TFIDF_WORDS = self._featurizer.get_feature_names()
        self.TFIDF_WEIGHT = tfidf.toarray()

        total_word_idf = dict(zip(self.TFIDF_WORDS, self.TFIDF_WEIGHT.sum(0).tolist())).items()
        total_word_idf.sort(key=lambda x: x[1], reverse=True)

        if word_length > 0:
            total_word_idf = filter(lambda x: len(x[0].decode('utf-8', 'ignore')) >= word_length, total_word_idf)

        if not return_tfidf_words_info:
            table = PrettyTable()
            table.field_names = ["Words", "TF-IDF"]
            for word, tf in total_word_idf:
                table.add_row((word, tf))
            table.sortby = "TF-IDF"
            table.align = 'l'
            table.reversesort = True
            print(table)
        else:
            return total_word_idf


    def do_tfidf(self, indocuments, word_length = None):
        '''
        使用此函数 fit 后 self._featurizer 为 CountVectorizer featurizer CountVectorizer
        :param indocuments:
        :param word_length:
        :return:
        '''
        if len(self._corpus) == 0 and len(indocuments) > 0:
            self.load_the_specimen(indocuments)

        if not len(self._corpus):
            print('没有任何语料输入')
            return None

        # 创建词频稀疏矩阵 结果对象为 scipy.sparse.coo_matrix
        self._featurizer = CountVectorizer()
        transformer = TfidfTransformer()
        # 根据文本词频矩阵 计算TF-IDF
        tfidf = transformer.fit_transform(self._featurizer.fit_transform(self._corpus))

        # 获取词袋模型中的所有词语
        self.TFIDF_WORDS = self._featurizer.get_feature_names()
        self.loger.debug('Words Total:{0}'.format(len(self.TFIDF_WORDS)))

        # 将TF-IDF矩阵抽取出来，元素w[m][n]表示n词在m标本中的tf-idf权重
        self.TFIDF_WEIGHT = tfidf.toarray()

        # 有多少维特征 调试降维效果
        self.loger.debug(
            '标本: {0} 维度: {1} 矩阵规模:[{2}][{3}]\n'.format(len(self.tag_list),
            len(self.TFIDF_WEIGHT[0]), len(self.tag_list), len(self.TFIDF_WEIGHT[0]))
        )

        total_word_idf = dict(zip(self.TFIDF_WORDS, self.TFIDF_WEIGHT.sum(0).tolist()))

        median_idf = sorted(total_word_idf.values())[len(total_word_idf) // 2]
        self.loger.info('median_idf: {0}'.format(median_idf))

        # word_list = sorted(vectorizer.vocabulary_.iteritems(), key = lambda x: x[1], reverse = True)
        table = PrettyTable()
        table.field_names = ["Words", "FREQ", "TF-IDF"]
        for word, tf in self._featurizer.vocabulary_.iteritems():
            # 这里的 word 是unicode
            if word_length is not None:
                if len(word) < word_length: continue`
            if tf < int(0.1*len(self._corpus)): continue
            table.add_row((word, tf, total_word_idf.get(word, None)))
        table.sortby = "TF-IDF"
        table.align = 'l'
        table.reversesort = True
        print(table)

    def get_vec(self, documents):
        return self._featurizer.transform(documents).toarray()


    def get_freq_dist(self, indocuments, word_length = None):
        if len(self._corpus) == 0 and len(indocuments) > 0:
            self.load_the_specimen(indocuments)

        if not len(self._corpus):
            print('没有任何语料输入')
            return None

        from itertools import chain

        fdist = FreqDist(chain.from_iterable(map(lambda x:x.split(),  self._corpus)))
        table = PrettyTable()
        table.field_names = ["Words", "Freq"]
        for word, tf in fdist.iteritems():
            if word_length is not None:
                if len(word.decode('utf-8', 'ignore')) < word_length: continue
                if globals().has_key('_PRODUCT_SET'):
                    if word not in globals()['_PRODUCT_SET']:
                        continue
            table.add_row((word, tf))
        table.sortby = "Freq"
        table.align = 'l'
        table.reversesort = True

        # self.loger.info("\n\n{0:-^38}\n\n{1}\n".format('词条详细信息：', str(table)))
        return table._rows


def test():
    indocuments = [
        'ONLY2017春装新品宽松T恤荷叶下摆两件套连衣裙女T|117161537 A01奶白 170/88A/L ',
        '粉红大布娃娃 新款女装长袖修身收腰喇叭袖连衣裙 D16CDR127 大红色 S ',
        '裂帛2017夏装新品V领刺绣松紧腰长裙子雪纺长袖连衣裙女51161608 花色2.0 L ',
        '森马收腰连衣裙 2017春季新款 女士甜美印花刺绣章仔裙子韩版潮女 本白1100 XS ',
        '菲梦伊2017新款蕾丝连衣裙女夏装中长包臀一步裙子显瘦优雅10951 铝灰色 S',
        '香影雪纺连衣裙 2017夏新款吊带蕾丝拼接碎花裙子收腰沙滩裙短袖 兰色 M ',
        '班尼路/Baleno夏男装 纯棉圆领短袖t恤男 小清新韩版潮流纯色体恤 02B中蓝 L',
        '百酷源 短袖t恤男2017夏季男士商务休闲拼色条纹修身上衣潮T101 白色 XL',
        '意树中国风原创亚麻休闲裤中式长裤男宽松直筒长裤子夏季棉麻男 灰色 大/175',

    ]


    T = TfidfVec()
    r = T.do_fit(indocuments)
    a = '中国风 原创 亚麻 休闲裤 中式 长裤 男 宽松 直筒 长裤子 夏季 棉麻'
    x = r.transform([a]).toarray()
    print(x)

if __name__ == '__main__':
    test()
    exit()


    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="原始标本文件")
    parser.add_argument("-k", "--kind", help="三级产品类", default=None, type=int)
    parser.add_argument("-d", "--diff", help="多个三级品类逗号隔开, 获取交叉词汇", default=None)
    parser.add_argument("-t", "--type", help="任务类型", default=1, type=int)
    parser.add_argument("-l", "--length", help="词条长度", default=None, type=int)

    def tobool(v):
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False

        return True

    parser.add_argument('-p', "--product", type=tobool, nargs='?', const=True, help="之分析产品词")

    args = parser.parse_args()

    task_type = args.type
    task_infile = args.infile
    kind = args.kind
    word_length = args.length
    only_product = args.product

    if only_product is None:
        only_product = False

    process_engine = None

    if task_type == 1:
        process_engine = "do_tfidf"
        # process_engine = "do_tfidf2"
    elif task_type == 2:
        process_engine = "get_freq_dist"
    elif task_type == 3:
        process_engine = ""
    else:
        parser.usage()

    if process_engine is None:
        exit()

    print(args)

    T = CorpusTfidf()
    from corpus_load import FileLoad

    if only_product:
        product_file = '/data1/product_audic_ok1.txt'
        # x = list(FileLoad(product_file))
        # print x
        globals()['_PRODUCT_SET'] = set(map(lambda y: y.split('\t')[0], filter(lambda x:x.strip(), FileLoad(product_file))))

    if task_type != 3:
        if kind is not None:
            indocuments = map(lambda y: y.split('\t')[1], filter(lambda x: x.split('\t')[0] == str(kind), FileLoad(task_infile)))
        else:
            indocuments = map(lambda y: y.split('\t')[1], FileLoad(task_infile))

        getattr(T, process_engine)(indocuments, word_length)
        # getattr(T, "do_tfidf2")(indocuments)

    else:
        diff_kinds = args.diff
        import sys
        if diff_kinds is None:
            print("未传入要对比的三级品类")
            sys.exit()

        diff_kinds = diff_kinds.split(',')
        if len(diff_kinds) != 2:
            print("对比品类格式为: kind1,kind2")
            sys.exit()

        docments1 =  map(lambda y: y.split('\t')[1], filter(lambda x: x.split('\t')[0] == diff_kinds[0], FileLoad(task_infile)))
        docments2 =  map(lambda y: y.split('\t')[1], filter(lambda x: x.split('\t')[0] == diff_kinds[1], FileLoad(task_infile)))

        doc1_tdidf_info = dict(T.do_tfidf2(docments1, word_length, True))
        T.reset()
        doc2_tdidf_info = dict(T.do_tfidf2(docments2, word_length, True))

        # 取两篇文档 核心名词 的交集
        intersection = []
        for k, v in doc1_tdidf_info.iteritems():
            if doc2_tdidf_info.has_key(k):
                intersection.append((k, v, doc2_tdidf_info[k]))

       


        table = PrettyTable()
        table.field_names = ["Words", "TF-IDF.{0}".format(diff_kinds[0]), "TF-IDF.{0}".format(diff_kinds[1])]
        for word, tf, tf1 in intersection:
            table.add_row((word, tf, tf1))
        table.sortby = "TF-IDF.{0}".format(diff_kinds[0])
        table.align = 'l'
        table.reversesort = True
        print(table)




