from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client=OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

# 聊天历史
messages=[]

while True:
    user_input = input("User: ")

    # 退出
    if user_input == "exit":
        break

    # 添加用户消息
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=messages
    )

    answer = response.output_text

    print(
        "Assistant:",
        answer
    )

    # 保存模型回答
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
