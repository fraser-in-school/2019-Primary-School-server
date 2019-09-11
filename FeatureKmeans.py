from sklearn.metrics import silhouette_score  # 引入评价函数
from sklearn.decomposition import PCA
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from PcapFeature import PcapFeature

projectPath = os.path.abspath('')

# dataPath = '/media/zhanghao/B6D488D4D48897EF/Users/zhanghao/Downloads/大文件/CompletePCAPs'


class FeatureKmeans:
    def __init__(self):
        self.files = None
        self.module = None
        self.trainSet = None
        self.dataPath = 'C:\\Users\\zhanghao\\Downloads\\大文件\\CompletePCAPs'
        self.get_data_file()
        self.read_data()

    # 获取目录下的所有文件名
    def get_data_file(self):
        self.files = os.listdir(self.dataPath)
        return self.files

    # 读取文件夹下的所有文件
    def read_data(self):
        pcap = PcapFeature()
        j = 0
        for file in self.files:
            ext = file.split('.')[1]
            if ext == 'pcap':
                filePath = os.path.join(self.dataPath, file)
                pcap.read_packet(filePath, 100)
            j += 1
            if j >= 20:
                break
        self.trainSet = pcap.get_DataFrame()

    def get_train_set(self):
        return self.trainSet

    def load_module(self, module='./module/module16'):
        self.module = joblib.load(module)

    def train(self, n, model=None, ):
        self.module = KMeans(n_clusters=n, n_jobs=-1)
        self.module.fit(self.get_train_set())
        return self.module

    def get_module(self):
        return self.module


def test():
    f_kmeans = FeatureKmeans()
    max = -1
    for k in range(5, 35, 3):
        f_kmeans.train(k)
        module = f_kmeans.get_module()
        score = silhouette_score(f_kmeans.get_train_set(), module.labels_)
        if score > max:
            joblib.dump(module, './module/feature-k=' + str(k) + '.pkl')


test()


