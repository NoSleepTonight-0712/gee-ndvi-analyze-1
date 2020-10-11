import ee
from IPython.display import Image
from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
import numpy as np
import ee.mapclient
import pprint
import pandas as pd

# 将影像的像素值转换为pandas 的DataFrame格式
def GetDataFrame(mc, band, coords):
    pnt = ee.Geometry.Point(coords)
    # Sample for a time series of values at the point.
    geom_values = mc.filterBounds(pnt).select(band).getRegion(geometry=pnt, scale=30)
    geom_values_list = ee.List(geom_values).getInfo()
    # Convert to a Pandas DataFrame.
    header = geom_values_list[0]
    data = pd.DataFrame(geom_values_list[1:], columns=header)
    data['datetime'] = pd.to_datetime(data['time'], unit='ms', utc=False)
    strTime = data.datetime.map(lambda x: x.strftime('%Y-%m-%d'))

    data['datetime'] = strTime

    data.set_index('time')
    data = data.sort_values('datetime')
    # print(data.columns)
    cls = ['datetime']
    nB = len(band)
    for b in band:
        cls.append(b)
    # print(cls)
    data = data[cls]
    return data
#计算区域的均值
def GetMeanRegion(mc,band,polygon):
    #pnt = ee.Geometry.Point(coords)
    # Sample for a time series of values at the point.
    #geom_values = mc.filterBounds(polygon).select(band).getRegion(geometry=polygon, scale=30)
    geom_values = mc.filterBounds(polygon).select(band).mean()
    geom_values_list = ee.List(geom_values).getInfo()
    # Convert to a Pandas DataFrame.
    header = geom_values_list[0]
    data = pd.DataFrame(geom_values_list[1:], columns=header)
    data['datetime'] = pd.to_datetime(data['time'], unit='ms', utc=True)
    data.set_index('time')
    data = data.sort_values('datetime')
    data = data[['datetime', band]]
    return data
def plotData(data):
    x =data.index
    y = data[data.columns[1]]
    plt.plot(x,y)