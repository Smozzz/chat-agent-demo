from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from openai import OpenAI
from dotenv import load_dotenv

import asyncio
import json
import os

load_dotenv()

openai_client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)


async def main():
    # 第一层：创建与MCP服务器的stdio连接
    async with stdio_client(server_params) as (read, write):
        # 第二层：基于这个连接创建会话
        async with ClientSession(read, write) as session:
            # 初始化会话（发送握手请求）
            await session.initialize()

            mcp_tools = await session.list_tools()
            print(mcp_tools)

            print("MCP Tools: ")

            openai_tools = []
            for tool in mcp_tools.tools:
                openai_tools.append(
                    {
                        "type": "function",
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                )

            history = []

            while True:

                # 用户输入
                user_input = input("\nUser:")
                history.append(
                    {
                        "role": "user",
                        "content": user_input
                    }
                )

                while True:

                    response = openai_client.responses.create(
                        model="gpt-5.4-mini",
                        input=history,
                        tools=openai_tools,
                    )

                    print("Model response: ", response.output)
                    history.extend(response.output)
                    tool_calls = [item for item in response.output
                                  if item.type == "function_call"]

                    if not tool_calls:
                        print("Assistant:", response.output_text)
                        break

                    for item in tool_calls:
                        name = item.name
                        args = json.loads(item.arguments)

                        # 调用mcp server

                        result = await session.call_tool(name, arguments=args)

                        print("Tool result: ", result)

                        # 结果返回LLM

                        history.append(
                            {
                                "type": "function_call_output",
                                "call_id": item.call_id,
                                "output": result.content[0].text
                            }
                        )


if __name__ == "__main__":
    asyncio.run(main())
