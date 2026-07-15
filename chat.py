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
    input="""
        分析下面简历。

        请只输出 JSON。
        
        姓名：Tom
        
        技能：
        Python
        Java
        Redis
    """
)

print(response.output_text)