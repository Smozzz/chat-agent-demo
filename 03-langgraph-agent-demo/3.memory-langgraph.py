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


load_dotenv()



# =====================
# 1. LLM
# =====================


llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# =====================
# 2. State
# =====================

class AgentState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]

# =====================
# 3. Node
# =====================

def chatbot(state:AgentState):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages":[
            response
        ]
    }

# =====================
# 4. Graph
# =====================

graph = StateGraph(
    AgentState
)

graph.add_node(
    "chatbot",
    chatbot
)

graph.set_entry_point(
    "chatbot"
)

graph.add_edge(
    "chatbot",
    END
)


# =====================
# 5. Memory
# =====================

memory = MemorySaver()

app = graph.compile(
    checkpointer=memory
)

# =====================
# 6. thread_id
# =====================

config = {

    "configurable":{
        "thread_id":
        "user_001"
    }

}



# 第一次聊天

result1 = app.invoke(

    {
        "messages":[
            HumanMessage(
                content=
                "我叫张三"
            )
        ]
    },

    config=config

)


print("第一次:")

print(
    result1["messages"][-1]
)

# 第二次聊天

result2 = app.invoke(

    {

        "messages":[

            HumanMessage(
                content=
                "我叫什么？"
            )

        ]

    },

    config=config

)

print("\n第二次:")

print(
    result2["messages"][-1]
)

print(result2)
