from pcap.proc.pcap import Pcap
from pcap.proc.pcap import PcapHead
from pcap.proc.util import BytesBuffer
from pcap.proc.packet import Packet
from pcap.proc.util import BytesOrder
import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.externals import joblib


projectPath = os.path.abspath('')
dataPath = os.path.join(projectPath, 'C:\\Users\\zhanghao\\Downloads\\大文件\\CompletePCAPs')

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
        if i >= 10:
            break


def train(n, train_data, model, ):
    km = KMeans(n_clusters=200)
    km.fit(pd.DataFrame(train_data))
    joblib.dump(km, './module/10.pkl')
    # print('labers')
    # print(km.labels_)
    # print('predict')
    # print(km.predict(pd.DataFrame(train_data)))
    # print('score')
    # print(km.inertia_)


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
        ext = file.split('.')[1]
        if ext == 'pcap':
            filePath = os.path.join(dataPath, file)
            get_train_set(dataFile=filePath, trainData=trainData)
        print(filePath)
        print(len(trainData))

    # getTrainSet()
    # train()

test()