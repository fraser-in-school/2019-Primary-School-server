# k-means聚类算法

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors
import sklearn.datasets as ds
from sklearn.cluster import KMeans  # 引入kmeans

inputfile="./1.xlsx"
outputfile="../out.xlsx"
data = pd.read_excel(inputfile) #读取数据

#模型构建
km=KMeans()
km.fit(data)
y_hat = km.predict(data)
print("所有样本距离聚簇中心点的总距离和:", km.inertia_)
print("距离聚簇中心点的平均距离:", (km.inertia_ / 400))
print("聚簇中心点:", km.cluster_centers_)

