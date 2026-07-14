from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client=OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client=OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)


while True:
    user_input = input("\nUser: ")

    # 退出
    if user_input == "exit":
        break


    stream = client.responses.create(
        model="gpt-5.4-mini",
        input=user_input,
        stream=True,
    )

    print("Assistant:",end="")

    for event in stream:

        if event.type == "response.output_text.delta":
            print(
                event.delta,
                end=""
            )