# -*- coding: utf-8 -*-

from pyecharts.charts import Pie,Line,Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://192.168.56.1:8000/static/js/"


def LineCharts(data):
    line = Line(init_opts=opts.InitOpts(width="100%"))
    line.add_xaxis(xaxis_data=[item[0] for item in data[1]])  # 设置x轴数据
    line.add_yaxis(
        series_name=data[0],
        y_axis=[item[1] for item in data[1]],
        yaxis_index=0,
        is_smooth=True,
        is_symbol_show=False,
        is_connect_nones=True,
    )  # 设置y轴数据
    title = data[0] + '使用率(%)'
    line.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[
            opts.DataZoomOpts(yaxis_index=0,range_start=0,range_end=100),
            opts.DataZoomOpts(type_="inside", yaxis_index=0),
        ],
        visualmap_opts=opts.VisualMapOpts(
            pos_top="10",
            pos_right="10",
            is_piecewise=True,
            pieces=[
                {"gt": 0, "lte": 25, "color": "#096"},
                {"gt": 25, "lte": 50, "color": "#ffde33"},
                {"gt": 50, "lte": 75, "color": "#ff9933"},
                {"gt": 75, "color": "#cc0033"},
            ],
            out_of_range={"color": "#999"},
        ),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name_location="start",
            min_=0,
            max_=100,
            is_scale=True,
            axistick_opts=opts.AxisTickOpts(is_inside=False),
        ),
    )
    line.set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                {"yAxis": 25},
                {"yAxis": 50},
                {"yAxis": 75},
            ],
            label_opts=opts.LabelOpts(position="end"),
        ))
    # line.render()#渲染图表，默认文件名为render.html
    return line.render_embed()

def MultipleLineCharts(datas):
    line = Line(init_opts=opts.InitOpts(width="100%"))
    line.add_xaxis(xaxis_data=[item[0] for item in datas[1][0][1]])  # 设置x轴数据
    for data in datas[1]:
        line.add_yaxis(
            series_name=data[0],
            y_axis=[item[1] for item in data[1]],
            yaxis_index=0,
            is_smooth=True,
            is_symbol_show=False,
            is_connect_nones=True,
        )  # 设置y轴数据

    line.set_global_opts(
        title_opts=opts.TitleOpts(title=datas['title']),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[
            opts.DataZoomOpts(yaxis_index=0,range_start=0,range_end=100),
            opts.DataZoomOpts(type_="inside", yaxis_index=0),
        ],
        visualmap_opts=opts.VisualMapOpts(
            pos_top="10",
            pos_right="10",
            is_piecewise=True,
            pieces=[
                {"gt": 0, "lte": 25, "color": "#096"},
                {"gt": 25, "lte": 50, "color": "#ffde33"},
                {"gt": 50, "lte": 75, "color": "#ff9933"},
                {"gt": 75, "color": "#cc0033"},
            ],
            out_of_range={"color": "#999"},
        ),
        xaxis_opts=opts.AxisOpts(type_="category"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name_location="start",
            min_=0,
            max_=100,
            is_scale=True,
            axistick_opts=opts.AxisTickOpts(is_inside=False),
        ),
    )
    line.set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                {"yAxis": 25},
                {"yAxis": 50},
                {"yAxis": 75},
            ],
            label_opts=opts.LabelOpts(position="end"),
        ))
    # line.render()#渲染图表，默认文件名为render.html
    return line.render_embed()

fn = """
    function(params) {
        if(params.name == '其他')
            return '\\n\\n\\n' + params.name + ' : ' + params.value + '%';
        return params.name + ' : ' + params.value + '%';
    }
    """

def new_label_opts():
    return opts.LabelOpts(formatter=JsCode(fn), position="center")

def MutiplePieCharts(datas):
    height_i = '450'
    if len(datas) > 3:
        height_i = height_i + (350 * (len(datas) // 3))
    height = str(height_i) + 'px'
    pie = Pie(init_opts=opts.InitOpts(width="100%",height=height))
    left_i = 1
    right_i = 1
    for data in datas:
        right = str(300 * right_i) + 'px'
        if left_i == 1:
            left = '20%'
            left_i = 2
        elif left_i == 2:
            left = '50%'
            left_i = 3
        else:
            left = '80%'
            right_i += 1
            left_i = 1
        pie.add(
            data[0],
            data[1],
            center=[left, right],
            radius=120,
        )
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="磁盘使用率"),

    )
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),)
    return pie.render_embed()

def BarCharts(datas):
    bar = Bar(init_opts=opts.InitOpts(width="100%"))
    bar.add_xaxis(datas[1])
    for data in datas[2]:
        bar.add_yaxis(data[0], data[1])
    # .add_yaxis("商家B", [20, 10, 40, 30, 40, 50])
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        title_opts=opts.TitleOpts(title=datas[0]),
    )
    return bar.render_embed()