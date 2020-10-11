import ee
from IPython.display import Image
from IPython.core.display import display, HTML
import matplotlib.pyplot as plt
import numpy as np
import ee.mapclient
import pprint
import pandas as pd
from matplotlib.figure import Figure

from Utils import *

ee.Initialize()

siteName = 'ARou'
siteLocation = [100.4643, 38.0473]

eePoint = ee.Geometry.Point(siteLocation)
fc = ee.Feature(eePoint, {'name': siteName, 'fill': 1})

i = 7  # i = 7 对应的是Landsat的NDVI 数据集
#可以使用的数据集列表
lstMCNames = ['LANDSAT/LC08/C01/T1','MODIS/006/MCD15A3H',
              'MODIS/006/MOD13A2','COPERNICUS/S2_SR',
              'MODIS/006/MOD13Q1','MODIS/006/MOD13A1',
              'MODIS/006/MOD09GA','LANDSAT/LC08/C01/T1_8DAY_NDVI']

images = ee.ImageCollection(lstMCNames[i]).filterDate('2013-07-01', '2020-10-10').filterBounds(eePoint)
bandNames = images.first().bandNames().getInfo()
print(bandNames)
print(images.size().getInfo())

firstImage = images.first().clip(eePoint)

Coords = [siteLocation]

outputData = pd.DataFrame()

for i, pn in enumerate(Coords):
    data = GetDataFrame(images, bandNames, pn)
    data['siteNumber'] = i
    outputData = outputData.append(data)

strFn = lstMCNames[i].replace('/', '_')
strFn = 'MYSELF_'+strFn + '_' + siteName + '.csv'
outputData.to_csv(strFn)
outputData.fillna(method = 'ffill',inplace = True)
plot = outputData.plot(x='datetime', y='NDVI', rot=45)
plt.tight_layout()
fig : Figure = plot.get_figure()
fig.savefig('./ndvi.png')
