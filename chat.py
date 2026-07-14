from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client=OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv('OPENAI_API_KEY'),
)

response = client.responses.create(
    model="gpt-5.4-mini",
    input="你好"
)


print(response.output_text)