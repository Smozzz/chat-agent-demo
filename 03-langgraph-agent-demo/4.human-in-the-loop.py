from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

from langchain_core.messages import (
    HumanMessage,
    BaseMessage
)

from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt

from tools import tools

load_dotenv()

# =====================
# LLM
# =====================


llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

llm=llm.bind_tools(tools=tools)

# =====================
# State
# =====================


class AgentState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

# =====================
# Node 1
# LLM
# =====================

def chatbot(state):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages":[
            response
        ]
    }


# =====================
# Node 2
# 人工审批
# =====================

def human_approval(state):


    last_message = (
        state["messages"][-1]
    )

    tool_call = (
        last_message.tool_calls[0]
    )

    decision = interrupt(
        {
            "question":
            "是否允许执行工具?",

            "tool":
            tool_call
        }
    )

    if decision != "yes":
        raise Exception("用户拒绝执行")

    return {}


# =====================
# 判断
# =====================


def check_tool(state):

    last = state["messages"][-1]

    if last.tool_calls:

        return "approval"


    return END

# =====================
# Graph
# =====================


graph = StateGraph(
    AgentState
)


graph.add_node(
    "chatbot",
    chatbot
)


graph.add_node(
    "approval",
    human_approval
)

graph.add_node(
    "tools",
    ToolNode(tools)
)


graph.set_entry_point(
    "chatbot"
)


graph.add_conditional_edges(
    "chatbot",
    check_tool
)

graph.add_edge(
    "approval",
    "tools",
)

graph.add_edge(
    "tools",
    "chatbot"
)
# =====================
# checkpoint
# =====================


memory = MemorySaver()

app = graph.compile(
    checkpointer=memory
)

# =====================
# thread
# =====================


config = {

    "configurable":{

        "thread_id":
        "email_task_001"

    }

}

# 第一次运行

result = app.invoke(
    {
        "messages":[

            HumanMessage(
                content=
                "帮我发送邮件给Tom，给他说我要晚点到，邮箱地址是12@12.com"
            )

        ]
    },
    config=config

)


print(result)
