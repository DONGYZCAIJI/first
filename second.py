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
            bar_size=1,#柱子大小
            shading="lambert",#阴影类型
            label_opts=opts.LabelOpts(
            is_show=False,
            ),
        ).set_global_opts( title_opts=opts.TitleOpts(
            title="2018年中国大陆机场航班数量专题图",#设置标题
            subtitle="",

        ),visualmap_opts=opts.VisualMapOpts(#设置图例，范围分段专题图
            is_piecewise=True,
            pieces=[
                {"min":800,"label":">800","color":'blue'},
                {"min":500,"max":799,"label":"500-799","color":'red'},
                {"min":200,"max":499,"label":"200-499","color":'peru'},
                {"min":100,"max":199,"label":"100-199","color":'orange'},
                {"min":10,"max":99,"label":"10-99","color":'gold'},
                {"min":0,"max":9,"label":"0-9","color":'cornsilk'},
            ])
        )
    )
    return c

df0=pd.read_excel('E:\延宗\大三上\国庆作业\gis开发作业\航班数据\国内航班数据new.xls')#读取航班数据
sizes=df0["departure_airport"].value_counts()#计数统计

df1=pd.DataFrame({'flights_amount':sizes})#数据格式转换
print(df1)

#获取各个出发机场的名称、坐标，去除重复数据
df2=df0[['departure_airport','departure_y','departure_x']].drop_duplicates()
#修改索引值为机场名，以便后续同‘flights_amount'（航线数量）合并
df2.index=df2['departure_airport']
#增加一列"flights_amounts"
df2['flights_amounts']=df1
#数据格式转换
city_lines=list(zip(df2['departure_airport'],list(zip(df2['departure_x'],
                         df2['departure_y'],df2['flights_amounts']))))
print(city_lines)

#调用函数，绘制三维地图
# airport_3D=map3d_with_bar3d(city_lines)
# airport_3D.render(path='机场三维分布图.html')