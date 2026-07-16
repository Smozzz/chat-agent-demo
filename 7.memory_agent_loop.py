from openai import OpenAI
from dotenv import load_dotenv
from tools import *
import json
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

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

history = []

while True:
    user_input = input("\nUser:")

    if user_input == "exit":
        break

    history.append({
        "role": "user",
        "content": user_input,
    })

    while True:
        print("history", history)
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=history,
            tools=tools,
        )

        print("response:", response)

        history.extend(response.output)

        tool_calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            print("Assistant:", response.output_text)
            break

        for tool_call in tool_calls:
            name = tool_call.name
            args = json.loads(tool_call.arguments)

            if name == "get_weather":
                result = get_weather(args["city"])
            elif name == "calculator":
                result = calculator(args["str1"])
            else:
                result = f"Unknown function: {name}"

            print("call_id", tool_call.call_id, "\noutput", result)

            history.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result),
            })