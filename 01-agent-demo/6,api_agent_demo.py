from openai import OpenAI
from dotenv import load_dotenv
from tools import *
import json
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

response = client.responses.create(
    model="gpt-5.4-mini",
    input="北京天气怎么样",
    tools=[
        {
            "type": "function",
            "name":"get_weather",
            "description":"查询指定城市天气",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    ]
)

print(response.output)

tool_call=response.output[0]

args = json.loads(
    tool_call.arguments
)

results=get_weather(args["city"])

