#!/usr/bin/python
#-*- coding: utf-8 -*-


# ********************************
#    FileName: VecSearch.py
#    Author  : ghostwwl
#    Email   : ghostwwl@gmail.com
#    Date    : 2019-7-15
#    Note    : 基于向量的检索 图片 和 文本 实现
# ********************************


__author__ = "ghostwwl"

#```
#1. 对象(text, image ...) --> vec
#    a. 这里我们得用一个 东西 保存 vec --> 对象 or 对象id
#2. vec --> faiss index
#3. 被检索对象 --> input vec
#4. input vec --> faiss index --> 一堆 vec/一堆 vec id
#5. 通过一堆 vec --> 一堆 对象
#```


# Index factory
# 用一个字符串构建Index，用逗号分割可以分为3部分：1.前处理部分；2.倒排表（聚类）；3.细化后处理部分
#
# 在前处理部分（preprocessing）：
# 1.PCA。"PCA64"表示通过PCA将数据维度降为64，"PCAR64"表示增加了随机旋转（random rotation）。
# 2.OPQ。"OPQ16"表示用OPQMatrix将数组量化为16位（待完善）
# 倒排表部分（inverted file）：
# 1."IVF4096"表示建立一个大小是4096的倒排表，即聚类为4096类。 细化部分（refinement）：
# 1."Flat"保存完整向量，通过IndexFlat或者IndexIVFFlat实现；
# 2."PQ16"将向量编码为16byte，通过IndexPQ或者IndexIVFPQ实现；
# index = index_factory(128, "PCA80,Flat") # 原始向量128维，用PCA降为80维，然后应用精确搜索
# index = index_factory(128, "OPQ16_64,IMI2x8,PQ8+16") #原始向量128维，用OPQ降为64维，分为16类，用2*8bit的倒排多索引，用PQ编码为8byte保存，检索时使用16byte。




import os
import faiss
import numpy as np


class BaseEngine(object):
    def save_index(self, index, index_save_file):
        return faiss.write_index(index, index_save_file)

    def load_index(self, index_save_file):
        return faiss.read_index(index_save_file)



class VecEngine(BaseEngine):
    def obj2vec(self, obj, obj_id: int):
        raise NotImplementedError

    def vec2obj(self, vec):
        raise NotImplementedError


#------------------------------------------------------------------
# 假设我这里用vgg16提取图片特征
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.models import Model

class ImageVecEngine(VecEngine):
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):  # img is from PIL.Image.open(path) or keras.preprocessing.image.load_img(path)
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        x = image.img_to_array(img)  # To np.array. Height x Width x Channel. dtype=float32
        x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = preprocess_input(x)  # Subtracting avg values for each pixel

        # preds = self.model.predict(x)
        # print('Predicted:', decode_predictions(preds, top=3)[0])

        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
        return feature / np.linalg.norm(feature)  # Normalize

    def obj2vec(self, img_file, img_id: int):
        img = image.load_img(img_file, target_size=(224, 224))
        return self.extract(img)

    def vec2obj(self, vec):
        pass



#------------------------------------------------------------------
class TextVecEngine(VecEngine):
    def __init__(self, pre_train_vec, embedding_size=300):
        self.embedding_size = embedding_size
        self.embedding_path = pre_train_vec
        self.embedding_dict = {}

    def load_vec(self):
        """
        加载训练好的文本类型词向量 可以是word2vec or glove
        :return:
        """
        count = 0
        with open(self.embedding_path) as embfile:
            for line in embfile:
                line = line.strip().split(' ')
                if len(line) < 300:
                    continue
                wd, vector = line[0], np.array([float(i) for i in line[1:]])
                self.embedding_dict[wd] = vector
                count += 1
                if count % 10000 == 0:
                    self.loger.info('{} loaded'.format(count))
        self.loger.info('loaded {} word embedding, finished'.format(count))

    def get_keywords(self, sentence):
        """
        对句子处理为词
        :param sentence:
        :return:
        """
        pass

    def obj2vec(self, sentence, doc_id):
        """
        这里是通过句子分词的 词向量  \freq {\sum_{i=0}_{m} V_{i}} {m}

        :param sentence:
        :param doc_id:
        :return:
        """

        # 对每个句子的所有词向量取均值，来生成一个句子的vector
        word_list = self.get_keywords(sentence)
        embedding = np.zeros(self.embedding_size)
        sent_len = 0
        for index, wd in enumerate(word_list):
            if wd in self.embdding_dict:
                embedding += self.embdding_dict.get(wd)
                sent_len += 1
            else:
                continue
        return embedding/sent_len, doc_id

    def vec2obj(self, vec):
        pass

#------------------------------------------------------------------
class Indexer(BaseObject):
    def pre_index(self):
        if not hasattr('add_with_ids', self.index):
            self.index = faiss.IndexIDMap(self.index)

    def add2inx(self, obj):
        pass

    def saveIndex(self, localpath):
        return faiss.write_index(self.index, localpath)
        pass

    def loadIndex(self, localpath):
        self.index = faiss.read_index(localpath)
        pass

    def mergeIndex(self, otherIndex):
        """
        索引合并
        :param other_index:
        :return:
        """
        # faiss.merge_into(otherIndex)
        self.index.merge_from(otherIndex, otherIndex.ntotal)
        return self.index.ntotal
        pass

#------------------------------------------------------------------
class Searcher(BaseObject):
    def search_byid(self, vid, topn=10):
        """
        根据 已知的向量编号搜索， 向量已存在索引中
        :param vid:     添加索引时，向量的编号
        :param topn:
        :return:
        """
        return self.search(self.reconstruct_vec(vid), topn)

    def search(self, vec, topn=10):
        """
        根据向量 vec 检索 返回 topn
        :param vec:
        :param topn:
        :return:    dis, inx = self.index.search(vec, 10)
        """
        return self.index.search(vec, topn)

    def search_byvid(self, vid, vid_start, vid_end):
        """
        搜索距离范围内的向量
        :param vid:         要查询的向量id
        :param vid_start:   向量的起始id
        :param vid_end:     向量的终止id
        :return:            返回结果是一个三元组，分别是limit(返回的结果的数量), distance, index
        """

        dist = float(np.linalg.norm(self.reconstruct_vec(vid_end) - self.self.reconstruct_vec(vid_start))) * 0.99  # 定义一个半径/阈值
        return self.index.range_search(self.reconstruct_vec(vid), dist)



#------------------------------------------------------------------
class BaseIndex(Indexer, Searcher):
    def remove(self, *ids):
        '''
        根据向量ids 从索引里删除
        :param ids:
        :return:
        '''
        self.index.remove_ids(np.array(ids))

    def reconstruct_vec(self, vid):
        '''
        根据向量id 获取向量
        :param vid:
        :return:
        '''
        return self.index.reconstruct(vid)




if __name__ == "__main__":
    pass
