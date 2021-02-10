#!/usr/bin/python
#-*- coding: utf-8 -*-

# ********************************
#    FileName: DocSpectralClustering.py
#    Author  : ghostwwl
#    Email   : ghostwwl@gmail.com
#    Date    : 2017-12-13
#    Note    :
# ********************************

__author__ = "ghostwwl"

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering, affinity_propagation
from sklearn import metrics
import jieba

# Spectral Clustering(SC,即谱聚类)，是一种基于图论的聚类方法,它能够识别任意形状的样本空间且收敛于全局最有解，
# 其基本思想是利用样本数据的相似矩阵进行特征分解后得到的特征向量进行聚类.它与样本特征无关而只与样本个数有关。

# 基本思路：将样本看作顶点,样本间的相似度看作带权的边,从而将聚类问题转为图分割问题:找到一种图分割的方法使得连接不同组的边的权重尽可能低
# (这意味着组间相似度要尽可能低),组内的边的权重尽可能高(这意味着组内相似度要尽可能高).


# Affinity Propagation Clustering是2007年在Science上发表的一篇single-exemplar-based的聚类方面的文章。特别适合高维、多类数据快速聚类，相比传统的聚类算法，从聚类性能和效率方面都有大幅度的提升。
#
# Affinity Propagation Clustering 可翻译为：仿射传播聚类，吸引子传播聚类，近邻传播聚类，相似性传播聚类，亲和力传播聚类，以下简称 AP聚类.优点有：
#
# 不需要指定最终聚类族的个数
# 已有的数据点作为最终的聚类中心，而不是新生成一个族中心
# 模型对数据的初始值不敏感
# 对初始相似度矩阵数据的对称性没有要求
# 相比于k-centers聚类方法，其结果的平方差误差较小
# AffinityPropagation 聚类方法是通过在样本对之间发送消息直到收敛来创建聚类。 然后使用少量示例样本作为聚类中心来描述数据集， 聚类中心是数据集中最能代表一类数据的样本。
#
# ​ 在样本对之间发送的消息表示一个样本作为另一个样本的示例样本的适合程度(suitability)，适合程度值再根据通信的反馈不断更新。更新迭代直到收敛，完成聚类中心的选取，因此也给出了最终聚类。
#
# ​ **与其他聚类算法的不同之处是，AP在开始时，将所有节点都堪看成是潜在的聚类中心。**然后通过节点间的通信，找出最合适的聚类中心，并将其他节点划分到这些中心下去。所以，目标是找到聚类中心；手段是通过节点间通信。



def test_spectral_clustering(documents):
    train_set = map(lambda x: ' '.join( jieba.cut(x) ), documents)
    # print(list(train_set))

    vectorizer = CountVectorizer()
    document_term_matrix = vectorizer.fit_transform(train_set)

    tfidf = TfidfTransformer()
    tfidf.fit(document_term_matrix)

    tf_idf_matrix = tfidf.transform(document_term_matrix)
    sim_matrix = cosine_similarity(tf_idf_matrix, tf_idf_matrix)


    print( sim_matrix )
    print( type(sim_matrix) )
    # 表示要聚4个类
    labels = SpectralClustering(4, affinity='precomputed').fit_predict(sim_matrix)
    print( "JUR:", labels )

    # result = dict(zip(documents, julei_result))
    result = dict(zip(documents, labels))

    result_list = list(result.items())
    result_list.sort(key=lambda x: x[1])

    for item in result_list:
        print( '{1}\t{0}'.format(*item) )


def test_affinity_propagation(documents):
    train_set = map(lambda x: ' '.join(jieba.cut(x)), documents)

    vectorizer = CountVectorizer()
    document_term_matrix = vectorizer.fit_transform(train_set)

    tfidf = TfidfTransformer()
    tfidf.fit(document_term_matrix)

    tf_idf_matrix = tfidf.transform(document_term_matrix)
    sim_matrix = cosine_similarity(tf_idf_matrix, tf_idf_matrix)

    cluster_centers_indices, labels, n_iter = affinity_propagation(sim_matrix, damping=0.75, max_iter=1000, convergence_iter=30, return_n_iter=True)
    print(cluster_centers_indices)
    print(labels)
    print(n_iter)

    # result = dict(zip(documents, julei_result))
    result = dict(zip(documents, labels))

    result_list = list(result.items())
    result_list.sort(key=lambda x: x[1])

    for item in result_list:
        print('{1}\t{0}'.format(*item))

# 聚类评估

## 1. 调整兰德系数 Adjusted Rand index
# RI 兰德系数  ARI 调整兰德系数 衡量两个分布的吻合程度
# RI [0, 1] ARI [-1, 1] 值越大 聚类结果与真实情况越吻合
# from sklearn import metrics
# >>> labels_true = [0, 0, 0, 1, 1, 1]
# >>> labels_pred = [0, 0, 1, 1, 2, 2]
#
# >>> ari = metrics.adjusted_rand_score(labels_true, labels_pred)

## 2.  互信息 Mutual Information based scores
# 有两种不同的标准化版本，即标准化互信息(NMI)和调整互信息(AMI)。NMI在文献中经常被使用，而AMI是最近才提出的，并且是随机规范化的

# NMI [0, 1] AMI [-1, 1]  都是 值越大 聚类结果与真实情况越吻合

# labels_true = [0, 0, 0, 1, 1, 1]
# >>> labels_pred = [0, 0, 1, 1, 2, 2]
# >>> nmi = metrics.normalized_mutual_info_score(labels_true, labels_pred)
# >>> ami = metrics.adjusted_mutual_info_score(labels_true, labels_pred)

## 3. Homogeneity, completeness and V-measure
# 同质性homogeneity：每个群集只包含单个类的成员。
# 完整性completeness：给定类的所有成员都分配给同一个群集。

# >>> from sklearn import metrics
# >>> labels_true = [0, 0, 0, 1, 1, 1]
# >>> labels_pred = [0, 0, 1, 1, 2, 2]
# >>> metrics.homogeneity_score(labels_true, labels_pred)
# 0.66...
# >>> metrics.completeness_score(labels_true, labels_pred)
# 0.42...
# 两者的调和平均V-measure：
# >>> metrics.v_measure_score(labels_true, labels_pred)



if __name__ == "__main__":
    indocuments = [
        '智能倒立机家用健身器材倒立器倒挂器健身运动倒挂机拉',
        '探路者软壳衣女秋冬新款户外保暖开衫女情侣款软壳衣',
        '皮室内外街球篮球',
        '户外新款男式软壳抓绒衣保暖透气防风外套徒步旅行登山休闲上衣',
        '伊莱蓮倒立机家用健身器材倒挂器增高器收腹器颈腰椎间盘长高拉伸倒立机可调节折叠机械倒立机 ',
        '篮球五号蓝球幼儿园宝宝专用幼儿体能训练考试球',
        '倒立机家用健身器材倒立器倒挂器材增高机腰椎颈椎牵引器',
        '短节矶竿套装轻碳素手竿硬海竿套装矶钓竿两用竿',
        '海竿套装钓鱼竿套装新手渔具套装组合',
    ]

    test_spectral_clustering(indocuments)
    print('-'*30)
    test_affinity_propagation(indocuments)
