from langchain_core.tools import tool

@tool
def get_weather(city:str)->str:
    """
    查询城市天气
    """

    return f"{city}今天晴天，30℃"



@tool
def calculator(expression:str)->str:
    """
    计算数学表达式
    """

    try:

        return str(
            eval(expression)
        )

    except Exception as e:

        return f"错误:{e}"


tools=[
    get_weather,
    calculator
]