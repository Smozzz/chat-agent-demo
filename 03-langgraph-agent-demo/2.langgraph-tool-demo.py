from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    BaseMessage,
    HumanMessage
)

from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.graph.message import (
    add_messages
)

from langgraph.prebuilt import ToolNode
from tools import tools


load_dotenv()

# =====================
# 1. 初始化LLM
# =====================

llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 绑定工具
llm_with_tools = llm.bind_tools(
    tools
)

# =====================
# 2. 定义State
# =====================

class AgentState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]


# =====================
# 3. LLM Node
# =====================

def chatbot(state:AgentState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages":[
            response
        ]
    }



# =====================
# 4. 判断下一步
# =====================

def should_continue(state:AgentState):

    last_message = (
        state["messages"][-1]
    )


    if last_message.tool_calls:

        return "tools"

    return END



# =====================
# 5. 创建Graph
# =====================

graph = StateGraph(
    AgentState
)

# 添加节点

graph.add_node(
    "chatbot",
    chatbot
)

graph.add_node(
    "tools",
    ToolNode(tools)
)

# 起点

graph.set_entry_point(
    "chatbot"
)

# 条件边

graph.add_conditional_edges(

    "chatbot",

    should_continue

)


# Tool执行后回LLM

graph.add_edge(

    "tools",

    "chatbot"

)

# 编译
app = graph.compile()

# =====================
# 6.运行
# =====================


result = app.invoke(

    {
        "messages":[

            HumanMessage(
                content=
                "北京天气怎么样？"
            )

        ]
    }

)



for msg in result["messages"]:

    print("================")

    print(msg)
