from tools import *


def contains_operator(expr):
    return any(op in expr for op in ['+', '-', '*', '/'])


def agent(user_input):
    if "天气" in user_input:

        if "北京" in user_input:
            result = get_weather("北京")

            return result

    if contains_operator(user_input):
        result = calculator(user_input)
        return result

    if "张三" in user_input:
        result = search_database(user_input)
        return result

    if "时间" in user_input:
        result = get_time()
        return result

    return "我暂时不知道"


print(
    agent("当前时间")
)
