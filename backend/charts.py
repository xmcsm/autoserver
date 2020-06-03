# -*- coding: utf-8 -*-

from pyecharts.charts import Bar,Line
from pyecharts import options as opts

from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/static/js/"


def LineCharts(cpudata,memdata):
    line = Line(init_opts=opts.InitOpts(width="100%"))
    line.add_xaxis(xaxis_data=[item[0] for item in cpudata])  # 设置x轴数据
    line.add_yaxis(
        series_name="CPU",
        y_axis=[item[1] for item in cpudata],
        yaxis_index=0,
        is_smooth=True,
        is_symbol_show=False,
    )  # 设置y轴数据
    line.add_yaxis(
        series_name="内存",
        y_axis=[item[1] for item in memdata],
        yaxis_index=0,
        is_smooth=True,
        is_symbol_show=False,
    )  # 设置y轴数据

    line.set_global_opts(
        title_opts=opts.TitleOpts(title="使用率(%)"),
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

