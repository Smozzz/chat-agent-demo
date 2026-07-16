from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather-server")

@mcp.tool()
def get_weather(city:str)->str:
    """
    查询城市天气
    """

    return f"{city}今天晴天，30℃"

@mcp.tool()
def calculator(expression: str) -> str:

    """
    数学计算
    """

    try:

        result = eval(expression)

        return str(result)

    except Exception as e:

        return f"计算错误:{e}"

if __name__=="__main__":

    mcp.run()