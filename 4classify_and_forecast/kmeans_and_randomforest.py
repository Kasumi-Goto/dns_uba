# -*- coding: utf-8 -*-
import list.list as list  # 自己的
import RF1.RF1 as RF1
import codecs
import csv
import sys
import matplotlib.pyplot as plt
import sklearn.neighbors
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA

clusters = sys.argv[1]

print("\n------------------------")
#########################################################################
#                           第一步 计算TFIDF
# 文档语料 空格连接
corpus = []

# 读取语料 一行语料为一个文档
for line in csv.reader(open('result.csv', 'r')):
    s = ','.join(line)
    corpus.append(s)

# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()

# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()

# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 打印特征向量文本内容
print('Features length: ' + str(len(word)))
resName = "Tfidf_Result(1).txt"
result = codecs.open(resName, 'w', 'utf-8')
for j in range(len(word)):
    result.write(word[j] + ' ')
result.write('\r\n\r\n')

# 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
for i in range(len(weight)):
    # print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    for j in range(len(word)):
        # print(weight[i][j])
        result.write(str(weight[i][j]) + ' ')
    result.write('\r\n\r\n')

result.close()

########################################################################
#                               第二步 聚类Kmeans

print('Start Kmeans:')
from sklearn.cluster import KMeans

clf = KMeans(n_clusters=int(clusters))
s = clf.fit(weight)
print(s)

# 每个样本所属的簇
label = []  # 存储1000个类标 4个类
# print(clf.labels_)
i = 1
while i <= len(clf.labels_):
    # print(i, clf.labels_[i - 1])
    label.append(clf.labels_[i - 1])
    i = i + 1

# 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
print(clf.inertia_)

j = 1
f1 = codecs.open('result.csv', 'r')
r_csv = csv.reader(f1)
f2 = open('kmeans_result.csv', 'w+', newline='')
w_csv = csv.writer(f2)
for line in r_csv:
    line.append(clf.labels_[j - 1])
    w_csv.writerow(line)
    j = j + 1
f2.close()
f1.close()

########################################################################
#                               第三步 图形输出 降维
pca = PCA(n_components=2)  # 输出两维
newData = pca.fit_transform(weight)  # 载入N维

x = []
y = []
for i in newData:
    x.append(i[0])
    y.append(i[1])

ax = plt.axes()
plt.scatter(x, y, c=clf.labels_, marker="o")
plt.xticks(())
plt.yticks(())
plt.savefig('kmeans.png')

print("\n------------------------")
list.main()
print("\n------------------------")
RF1.main()
