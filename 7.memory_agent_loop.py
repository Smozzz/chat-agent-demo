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

            # if name == "get_weather":
            #     result = get_weather(args["city"])
            # elif name == "calculator":
            #     result = calculator(args["str1"])
            # else:
            #     result = f"Unknown function: {name}"

            # tool registry

            result=None
            if name in tool_map:
                function=tool_map[name]
                try:
                    result = function(**args)
                except Exception as e:
                    result = f"Tool {name} run failed: {e}"
            else:
                result = f"Tool {name} not found"

            print("call_id", tool_call.call_id, "\noutput", result)

            history.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result),
            })