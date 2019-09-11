from pcap.proc.pcap import Pcap
from pcap.proc.pcap import PcapHead
from pcap.proc.util import BytesBuffer
from pcap.proc.packet import Packet
from pcap.proc.util import BytesOrder
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score  # 引入评价函数
from sklearn.decomposition import PCA
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib

projectPath = os.path.abspath('')
dataPath = '/media/zhanghao/B6D488D4D48897EF/Users/zhanghao/Downloads/大文件/CompletePCAPs'


class BinaryKmeans:
    def __init__(self):
        self.files = None
        self.module = None
        self.dataPath = 'C:\\Users\\zhanghao\\Downloads\\大文件\\CompletePCAPs'
        self.trainData = []
        self.get_data_file()
        self.read_data()

    # 获取目录下的所有文件名
    def get_data_file(self):
        self.files = os.listdir(self.dataPath)
        return self.files

    def read_data(self):
        for file in self.files:
            ext = file.split('.')[1]
            if ext == 'pcap':
                filePath = os.path.join(self.dataPath, file)
                self.read_packet(filePath, 500)

    # 读取单个文件里面的前100个packet
    def read_packet(self, file, pktNum=500, byteNum=100):
        _pcap = Pcap()
        _gen = _pcap.parse(file)
        i = 0
        for pkt in _gen:
            data = bytearray(pkt.data)
            length = len(data)
            # 长度不足byteNum用0补齐，超过100取前100
            if length < byteNum:
                data = data + bytes([0] * (byteNum - length))
                self.trainData.append(data)
            else:
                self.trainData.append(data[:byteNum])
            # 读取所有 dataFile 文件里面的前pktNum个packet
            i += 1
            if i >= pktNum:
                break

    def get_train_set(self):
        return pd.DataFrame(self.trainData)

    def train(self, k):
        self.module = KMeans(n_clusters=k, n_jobs=-1)
        self.module.fit(self.get_train_set())
        joblib.dump(self.module, './module/500-1.pkl')

    def get_module(self):
        return self.module


def test():
    b_kmeans = BinaryKmeans()
    b_kmeans.train(50)


test()