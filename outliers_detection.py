#!/usr/bin/python
#-*- coding: utf-8 -*-

# ********************************
#    FileName: outliers_detection.py
#    Author  : ghostwwl
#    Email   : ghostwwl@gmail.com
#    Note    :
# ********************************

__author__ = "ghostwwl"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #导入绘图库

from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

# 分布的处理
# 对于高斯分布的数据，直接运用以上算法就好。
# 但是对于非高斯分布的数据，虽然也可是使用上面的算法，但是效果不是很好，所以我们尽量将非高斯分布转化成（近似）高斯分布，然后再进行处理。
# 数据整体偏小，可以求 ln(x) 或者 x^a, 0<a<1
# 数据整体偏大，可以求 e^a 或者 x^a, a>1


# Fitting an elliptic envelope是一个玩具；
#
# if 训练集很干净：
#      使用one-class svm；
# else:
#      if 能保证训练集能基本覆盖正常样本：
#           使用LOF；
#      else:
#           使用isolation forest；
#

#----------------------------------------------------------------------------------------------------------------------

def local_outlier_factor():
    # Local Outlier Factor（局部异常 系数/因子）
    X = [[-1.1], [0.2], [101.1], [0.3]]
    clf = LocalOutlierFactor(n_neighbors=2)
    return clf.fit_predict(X)
    # array([1, 1, -1, 1])
    # clf.negative_outlier_factor_
    # array([-0.9821..., -1.0370..., -73.3697..., -0.9821...])


def oneclass_svm():
    # 单类别的SVM
    X_train = X_train_demo.values
    # 构造分类器
    clf = svm.OneClassSVM(nu=0.2, kernel="rbf", gamma=0.2)
    clf.fit(X_train)
    # 预测，结果为-1或者1
    labels = clf.predict(X_train)
    # 分类分数
    score = clf.decision_function(X_train) # 获取置信度
    # 获取正常点
    X_train_normal = X_train[labels>0]


def isolation_forest():
    # iForest （Isolation Forest）孤立森林
    rng = np.random.RandomState(42)

    # 构造训练样本
    n_samples = 200  # 样本总数
    outliers_fraction = 0.25  # 异常样本比例
    n_inliers = int((1. - outliers_fraction) * n_samples)
    n_outliers = int(outliers_fraction * n_samples)

    X = 0.3 * rng.randn(n_inliers // 2, 2)
    X_train = np.r_[X + 2, X - 2]  # 正常样本
    X_train = np.r_[X_train, np.random.uniform(low=-6, high=6, size=(n_outliers, 2))]  # 正常样本加上异常样本

    # fit the model
    # max_samples 构造一棵树使用的样本数，输入大于1的整数则使用该数字作为构造的最大样本数目，
    # 如果数字属于(0,1]则使用该比例的数字作为构造iforest
    # outliers_fraction 多少比例的样本可以作为异常值
    clf = IsolationForest(behaviour='new', max_samples=0.8, contamination=0.25)
    clf.fit(X_train)
    # y_pred_train = clf.predict(X_train)
    scores_pred = clf.decision_function(X_train)
    threshold = np.percentile(scores_pred, 100 * outliers_fraction)  # 根据训练样本中异常样本比例，得到阈值，用于绘图

    ## 以下两种方法的筛选结果，完全相同
    X_train_predict1 = X_train[clf.predict(X_train) == 1]
    X_train_predict2 = X_train[scores_pred >= threshold, :]
    # 其中，1的表示非异常点，-1的表示为异常点
    clf.predict(X_train)


#----------------------------------------------------------------------------------------------------------------------
def three_sigma_outliers(data_x, data_y):
    # 基于3sigma的异常值检测
    n = 3 # n*sigma
    ymean = np.mean(data_y)     # 均值
    ystd = np.std(data_y)       # 计算标准差
    threshold1 = ymean - n * ystd
    threshold2 = ymean + n * ystd

    outlier = [] #将异常值保存
    outlier_x = []

    for i in range(0, len(data_y)):
        if (data_y[i] < threshold1) | (data_y[i] > threshold2):
            outlier.append(data_y[i])
            outlier_x.append(data_x[i])
        else:
            continue

    print('\n异常数据如下：\n')
    print(outlier)
    print(outlier_x)

    plt.plot(data_x, data_y)
    plt.plot(outlier_x, outlier, 'ro')
    for j in range(len(outlier)):
        plt.annotate(outlier[j], xy=(outlier_x[j], outlier[j]), xytext=(outlier_x[j], outlier[j]))
    plt.show()


#----------------------------------------------------------------------------------------------------------------------
def box_outliers(data_x, data_y):
    statistics = data_y.describe()  # 保存基本统计量
    IQR = statistics.loc['75%'] - statistics.loc['25%']  # 四分位数间距
    QL = statistics.loc['25%']  # 下四分位数
    QU = statistics.loc['75%']  # 上四分位数
    threshold1 = QL - 1.5 * IQR  # 下阈值
    threshold2 = QU + 1.5 * IQR  # 上阈值
    outlier = []  # 将异常值保存
    outlier_x = []

    for i in range(0, len(data_y)):
        if (data_y[i] < threshold1) | (data_y[i] > threshold2):
            outlier.append(data_y[i])
            outlier_x.append(data_x[i])
        else:
            continue

    print('\n异常数据如下：\n')
    print(outlier)
    print(outlier_x)

    plt.plot(data_x, data_y)
    plt.plot(outlier_x, outlier, 'ro')
    for j in range(len(outlier)):
        plt.annotate(outlier[j], xy=(outlier_x[j], outlier[j]), xytext=(outlier_x[j], outlier[j]))
    plt.show()

#----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    pass
