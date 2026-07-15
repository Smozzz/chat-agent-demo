import datetime

import numexpr as ne

def get_weather(city):
    """
    模拟查询城市天气tool
    :param city: 城市名
    :return: 城市天气情况
    """

    weather_data= {
        "北京": "晴天，30℃",

        "上海": "多云，28℃",

        "广州": "小雨，26℃"
    }

    return weather_data.get(city,"未知城市")

def calculator(str1):
    """
    计算器tool
    :param str1:
    :return:
    """
    return ne.evaluate(str1)

def search_database(name):
    """
    模拟查找数据库tool
    :param name:
    :return:
    """
    database=[
        {"name": "张三", "age": 20, "major": "CS"},
        {"name": "李四", "age": 38, "major": "CS"},
        {"name": "王五", "age": 25, "major": "CS"},
        {"name": "赵六", "age": 28, "major": "CS"}
    ]

    return [item for item in database if item["name"] == name]

def get_time():
    """
    当前时间tool
    :return:
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")