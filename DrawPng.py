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
from Binary import BinaryKmeans
from FeatureKmeans import FeatureKmeans

class DrawPng:
    def __init__(self):
        self.module = None
        self.data = None

    def dim_reduction(self, trainData):
        # 主成分提取降维
        pcaClf = PCA(n_components=3, whiten=True)
        pcaClf.fit(trainData)
        # 降维后的数据
        self.data = pcaClf.transform(trainData)

    def draw_plot(self, km):
        j = 0
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # km = joblib.load('./module/100.pkl')
        label_pred = km.labels_  # 获取聚类标签
        mark = ['aliceblue',
                'antiquewhite',
                'aqua',
                'aquamarine',
                'azure',
                'beige',
                'bisque',
                'black',
                'blanchedalmond',
                'blue',
                'blueviolet',
                'brown',
                'burlywood',
                'cadetblue',
                'chartreuse',
                'chocolate',
                'coral',
                'cornflowerblue',
                'cornsilk',
                'crimson',
                'cyan',
                'darkblue',
                'darkcyan',
                'darkgoldenrod',
                'darkgray',
                'darkgreen',
                'darkkhaki',
                'darkmagenta',
                'darkolivegreen',
                'darkorange',
                'darkorchid',
                'darkred',
                'darksalmon',
                'darkseagreen',
                'darkslateblue',
                'darkslategray',
                'darkturquoise',
                'darkviolet',
                'deeppink',
                'deepskyblue',
                'dimgray',
                'dodgerblue',
                'firebrick',
                'floralwhite',
                'forestgreen',
                'fuchsia',
                'gainsboro',
                'ghostwhite',
                'gold',
                'goldenrod',
                'gray',
                'green',
                'greenyellow',
                'honeydew',
                'hotpink',
                'indianred',
                'indigo',
                'ivory',
                'khaki',
                'lavender',
                'lavenderblush',
                'lawngreen',
                'lemonchiffon',
                'lightblue',
                'lightcoral',
                'lightcyan',
                'lightgoldenrodyellow',
                'lightgreen',
                'lightgray',
                'lightpink',
                'lightsalmon',
                'lightseagreen',
                'lightskyblue',
                'lightslategray',
                'lightsteelblue',
                'lightyellow',
                'lime',
                'limegreen',
                'linen',
                'magenta',
                'maroon',
                'mediumaquamarine',
                'mediumblue',
                'mediumorchid',
                'mediumpurple',
                'mediumseagreen',
                'mediumslateblue',
                'mediumspringgreen',
                'mediumturquoise',
                'mediumvioletred',
                'midnightblue',
                'mintcream',
                'mistyrose',
                'moccasin',
                'navajowhite',
                'navy',
                'oldlace',
                'olive',
                'olivedrab',
                'orange',
                'orangered',
                'orchid',
                'palegoldenrod',
                'palegreen',
                'paleturquoise',
                'palevioletred',
                'papayawhip',
                'peachpuff',
                'peru',
                'pink',
                'plum',
                'powderblue',
                'purple',
                'red',
                'rosybrown',
                'royalblue',
                'saddlebrown',
                'salmon',
                'sandybrown',
                'seagreen',
                'seashell',
                'sienna',
                'silver',
                'skyblue',
                'slateblue',
                'slategray',
                'snow',
                'springgreen',
                'steelblue',
                'tan',
                'teal',
                'thistle',
                'tomato',
                'turquoise',
                'violet',
                'wheat',
                'white',
                'whitesmoke',
                'yellow',
                'yellowgreen']
        for i in label_pred:
            ax.scatter([self.data[j:j + 1, 0]], [self.data[j:j + 1, 1]], [self.data[j:j + 1, 1]], mark[i])
            j += 1
        plt.show()


def test():
    # b_kmeans = BinaryKmeans()
    # b_kmeans.train(50)
    f_kmeans = FeatureKmeans()
    f_kmeans.train(20)
    draw = DrawPng()
    draw.dim_reduction(f_kmeans.get_train_set())
    draw.draw_plot(f_kmeans.get_module())

test()