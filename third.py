import numpy as np
import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

def map3d_with_bar3d(example_data)->Map3D:
    c=(
        Map3D().add_schema(itemstyle_opts=opts.ItemStyleOpts(#设置三维地图的样式
            color="rgb(15,101,123)",#地图背景颜色
            opacity = 1, #透明度
            border_width = 0.8,#边界宽度
            border_color="rgb(62,215,213)",#边界颜色
        ),
        map3d_label = opts.Map3DLabelOpts(
            is_show=False,#是否显示标记
        ),
        emphasis_label_opts=opts.LabelOpts(
            is_show=False,
            color="#fff",
            font_size=10,
            background_color="rgba(0,23,11,0)",
        ),
        light_opts=opts.Map3DLightOpts(#设置地图光线效果
            main_color="#fff",
            main_intensity=1.2,
            main_shadow_quality="high",
            is_main_shadow=False,
            main_beta=10,
            ambient_intensity=0.3,
        ),
    ).add(#添加一个图形
        series_name="",#设置图形名称
            data_pair=example_data,#指定数据源
            type_=ChartType.BAR3D,#设定图类型为三维柱状图
            bar_size=3,#柱子大小
            shading="lambert",#阴影类型
            label_opts=opts.LabelOpts(
            is_show=False,
            ),
        ).set_global_opts( title_opts=opts.TitleOpts(
            title="2021年中国大陆各省GDP总量图",#设置标题
            subtitle="",

        ),visualmap_opts=opts.VisualMapOpts(#设置图例，范围分段专题图
            is_piecewise=True,
            pieces=[
                {"min":100000,"label":">100000","color":'blue'},
                {"min":80000,"max":99999,"label":"80000-99999","color":'red'},
                {"min":50000,"max":79999,"label":"50000-79999","color":'peru'},
                {"min":20000,"max":59999,"label":"20000-59999","color":'orange'},
                {"min":10000,"max":19999,"label":"10000-19999","color":'gold'},
                {"min":2000,"max":9999,"label":"2000-9999","color":'cornsilk'},
            ])
        )
    )
    return c

df0=pd.read_excel(r'E:\pythonProject\firstHomework\data.xls')#读取航班数据
sizes=df0["rank"].value_counts()#计数统计
#获取各个出发机场的名称、坐标，去除重复数据
df2=df0[['name','lat','lon','money']].drop_duplicates()
#数据格式转换
city_lines=list(zip(df2['name'],list(zip(df2['lat'],df2['lon'],df2['money']))))
print(city_lines)


money_3D=map3d_with_bar3d(city_lines)
money_3D.render(path='2021年各省GDP排行榜.html')
print("done")