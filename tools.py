import datetime

import numexpr as ne

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "查询指定城市天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称",
                }
            },
            "required": ["city"],
        },
    },
    {
        "type": "function",
        "name": "calculator",
        "description": "可以进行简单加减乘除的数值计算",
        "parameters": {
            "type": "object",
            "properties": {
                "str1": {
                    "type": "string",
                    "description": "要计算的表达式",
                }
            },
            "required": ["str1"],
        },
    },
]

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
    result = ne.evaluate(str1)
    if hasattr(result, "item"):
        return result.item()

    return result

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

tool_map={
    "get_weather": get_weather,
    "calculator": calculator,
    "search_database": search_database,
    "get_time": get_time
}