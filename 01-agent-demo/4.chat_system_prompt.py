from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client=OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

messages=[
    # {
    #     "role":"developer",
    #     "content":"你是一名AI Agent专家。每次回答开头必须说：【AI Agent导师】"
    # }
]

while True:
    user_input = input("\nUser: ")

    # 退出
    if user_input == "exit":
        break

    messages.append(
        {
        "role":"user",
        "content":user_input
        }
    )

    stream = client.responses.create(
        model="gpt-5.4-mini",
        instructions="你是一名AI Agent专家。每次回答开头必须说：【AI Agent导师】",
        input=messages,
        stream=True
    )

    print("Assistant:",end="")

    answer = ""
    for event in stream:
        if event.type == "response.output_text.delta":
            delta = event.delta
            answer+=delta
            print(
                delta,
                end=""
            )

    messages.append(
        {
            "role":"assistant",
            "content":answer
        })