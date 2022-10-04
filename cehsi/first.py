#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 22/10/1 上午9:27
# @Author  : yanzong
# @File    : first.py
# 1、利用geopandas类库加载显示任意地区的矢量数据（shp或geojson格式），提交结果图；
# 2、利用pyecharts类库实现深圳市地铁线路可视化，提交结果HTML文件；
# 3、利用pyecharts、geopandas等类库实现中国大陆各省份某社会经济指标（例如人口、GDP等）的三维地图效果，数据年份自行决定，提交结果HTML文件；
# 以上题目3选2，完成后请将结果压缩为学号+姓名，在线提交。截止时间：10月8日23点。压缩文件如图所示：
# import geopandas
# import matplotlib.pyplot as plt
# import pyecharts
#
#
# world = geopandas.read_file(r"E:\new\countries.geojson")
# world.plot()
# #plt.savefig('./test1.png')
# plt.show()
# print(pyecharts.__version__)
# # #data = gpd.read_file('shapefile/china.gdb', layer='province')#读取gdb中的矢量数据
# # print(data.crs)  # 查看数据对应的投影信息
# # print(data.head())  # 查看前5行数据
# # data.plot()
# # plt.show()#简单展示
# coding:utf-8
import requests
import json
import pprint
import math
from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType

url = 'http://map.amap.com/service/subway?_1615494473615&srhdata=4403_drw_shenzhen.json'
response = requests.get(url)
result = json.loads(response.text)
stations = []
for i in result['l']:
    station = []
    for a in i['st']:
        station.append([float(b) for b in a['sl'].split(',')])
    stations.append(station)
pprint.pprint(stations)
# 需要的两个常量先设置好
pi = 3.1415926535897932384  # π
r_pi = pi * 3000.0 / 180.0
#转换坐标函数
def gcj02_bd09(lon_gcj02, lat_gcj02):
    b = math.sqrt(lon_gcj02 * lon_gcj02 + lat_gcj02 * lat_gcj02) + 0.00002 * math.sin(lat_gcj02 * r_pi)
    o = math.atan2(lat_gcj02, lon_gcj02) + 0.000003 * math.cos(lon_gcj02 * r_pi)
    lon_bd09 = b * math.cos(o) + 0.0065
    lat_bd09 = b * math.sin(o) + 0.006
    return [lon_bd09, lat_bd09]
result = []
for station in stations:
    result.append([gcj02_bd09(*point) for point in station])
map_b = (
    BMap(init_opts=opts.InitOpts(width="800px", height="600px"))
        .add_schema(
        baidu_ak='NyTBUR7qAlU8mt0PzSZwRNB4hX64SzVA',  # 百度地图开发应用appkey
        center=[116.403963, 39.915119],  # 当前视角的中心点
        zoom=10,  # 当前视角的缩放比例
        is_roam=True,  # 开启鼠标缩放和平移漫游
    )
        .add(
        series_name="",
        type_=ChartType.LINES,  # 设置Geo图类型
        data_pair=result,  # 数据项
        is_polyline=True,  # 是否是多段线，在画lines图情况下#
        linestyle_opts=opts.LineStyleOpts(color="blue", opacity=0.5, width=1),  # 线样式配置项
    )
        .add_control_panel(
        maptype_control_opts=opts.BMapTypeControlOpts(type_=BMapType.MAPTYPE_CONTROL_DROPDOWN),  # 切换地图类型的控件
        scale_control_opts=opts.BMapScaleControlOpts(),  # 比例尺控件
        overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),  # 添加缩略地图
        navigation_control_opts=opts.BMapNavigationControlOpts()  # 地图的平移缩放控件
    )
)

map_b.render(path='subway_shenzhen.html')