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

# 获取目录下的所有文件名
def get_data_file(dataPath):
    files = os.listdir(dataPath)
    return files


# 读取单个文件里面的前100个packet
def get_train_set(dataFile, trainData):
    _pcap = Pcap()
    _gen = _pcap.parse(dataFile)
    i = 0
    for pkt in _gen:
        data = bytearray(pkt.data)
        length = len(data)
        # 长度不足100用0补齐，超过100取前100
        if length < 100:
            data = data + bytes([0] * (100 - length))
            trainData.append(data)
        else:
            trainData.append(data[:100])
        # 读取所有 dataFile 文件里面的前100个packet
        i += 1
        if i >= 500:
            break


def train(n, trainData, model=None, ):
    km = KMeans(n_clusters=n, n_jobs=-1)
    km.fit(pd.DataFrame(trainData))
    joblib.dump(km, './module/500-0.pkl')
    return km
    # print('labers')
    # print(km.labels_)
    # print('predict')
    # print(km.predict(pd.DataFrame(train_data)))
    # print('score')
    # print(km.inertia_)


def dim_reduction(trainData):
    # 主成分提取降维
    pcaClf = PCA(n_components=3, whiten=True)
    pcaClf.fit(trainData)
    # 降维后的数据
    data = pcaClf.transform(trainData)
    return data

def parse(file, buffSize=2048):
    """
    解析pcap文件,返回值为一个生成器 yield
    :param file:缓冲文件大小
    :param buffSize:
    :return:返回一个生成器（用于处理大包）
    """
    assert file != ""
    _buff = BytesBuffer()
    _packet = None
    __head = None
    ret = 0
    with open(file, "rb") as o:
        ctx = None
        while 1:
            # 优先处理缓冲区数据(如果缓存数据超过了指定大小)
            bsize = len(_buff)
            if bsize > 0:
                if bsize >= buffSize:
                    ctx = _buff.getvalue()
                else:
                    _buff.write(o.read(buffSize))
                    ctx = _buff.getvalue()
                _buff.clear()
            else:
                ctx = o.read(buffSize)
            size = len(ctx)
            if size > 0:
                if __head is None:
                    # 文件头占24字节
                    if size >= 24:
                        __head = PcapHead(ctx[:24])
                        size -= 24
                        ctx = ctx[24:]
                    else:
                        _buff.write(ctx)
                # 分析包头(包头占16字节)
                if size > 16:
                    if _packet is None:
                        _packet = Packet()
                        ctx, size = _packet.parse(ctx)
                        if _packet.finish():
                            yield _packet
                            ret += 1
                            _packet = None
                        if size > 0:
                            _buff.write(ctx)
                    else:
                        ctx, size = _packet.parse(ctx)
                        if _packet.finish():
                            yield _packet
                            ret += 1
                            _packet = None
                        if size > 0:
                            _buff.write(ctx)
                else:
                    _buff.write(ctx)
            else:
                break
        del ctx
    del _buff

def test():
    files = get_data_file(dataPath)
    trainData = []
    filePath = ''
    for file in files:
        print(file)
        ext = file.split('.')[1]
        if ext == 'pcap':
            filePath = os.path.join(dataPath, file)
            get_train_set(dataFile=filePath, trainData=trainData)
    # k = []
    # score = []
    print('length:')
    print(len(trainData))
    # for i in range(5, 200, 5):
    #     km = train(i, trainData)
    #     k.append(i)
    #     score.append(km.inertia_)
    # plt.scatter(k, score)
    # plt.plot(k, score)
    # plt.xlabel("k")
    # plt.ylabel("distance")
    # plt.show()
    km = train(50, trainData)
    data = dim_reduction(trainData)
    drawPlot(data, km=km)
    # getTrainSet()
    # train()

def drawPlot(data, km):
    j = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # km = joblib.load('./module/100.pkl')
    label_pred = km.labels_  # 获取聚类标签
    centroids = km.cluster_centers_  # 获取聚类中心
    inertia = km.inertia_  # 获取聚类准则的总和
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
        ax.scatter([data[j:j + 1, 0]], [data[j:j + 1, 1]], [data[j:j + 1, 1]], mark[i])
        j += 1
    plt.show()

def load_module(module=None):
    km = joblib.load('./module/500-0.pkl')
    file = os.path.join(dataPath, 'aim_chat_3a.pcap')
    _pcap = Pcap()
    _gen = _pcap.parse(file)
    i = 0
    testData = []
    for pkt in _gen:
        data = bytearray(pkt.data)
        length = len(data)
        # 长度不足100用0补齐，超过100取前100
        if length < 100:
            data = data + bytes([0] * (100 - length))
            testData.append(data)
        else:
            testData.append(data[:100])
        # 读取所有 dataFile 文件里面的前100个packet
        i += 1
        if i >= 100:
            break
    return km.predict(pd.DataFrame(testData))
# test()

load_module()


