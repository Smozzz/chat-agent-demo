from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv("OPENAI_BASE_URL")
)


# ====================
# 1. 定义State
# ====================


class AgentState(TypedDict):

    messages:list


# ====================
# 2. 定义Node
# ====================


def chatbot(state:AgentState):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages":
        state["messages"]
        +
        [
            response
        ]
    }

# ====================
# 3. 创建Graph
# ====================

graph = StateGraph(
    AgentState
)

# 添加节点
graph.add_node(
    "chatbot",
    chatbot
)

# 起点
graph.set_entry_point(
    "chatbot"
)

# 终点
graph.add_edge(
    "chatbot",
    END
)

# 编译
app = graph.compile()

# ====================
# 4.运行
# ====================

result = app.invoke(
    {
        "messages":[
            (
                "user",
                "介绍一下Transformer"
            )
        ]
    }
)

print(result)

for msg in result["messages"]:

    print(msg)
