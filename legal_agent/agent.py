# legal_agent/agent.py
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from dotenv import load_dotenv
from legal_agent.tool_graph import search_graph_tool
import os
from openai import AzureOpenAI
from typing import TypedDict
load_dotenv()

# Kiểm tra các biến môi trường
# print("AZURE_ENDPOINT:", os.getenv("AZURE_ENDPOINT"))
# print("AZURE_API_KEY:", os.getenv("AZURE_API_KEY"))
# print("AZURE_API_VERSION:", os.getenv("AZURE_API_VERSION"))
# print("AZURE_OPENAI_CHAT_MODEL_NAME:", os.getenv("AZURE_OPENAI_CHAT_MODEL_NAME"))
# print("AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT:", os.getenv("AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT"))
# print("AZURE_OPENAI_EMBED_MODEL_NAME:", os.getenv("AZURE_OPENAI_EMBED_MODEL_NAME"))
# print("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT:", os.getenv("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT"))

# ✅ Khởi tạo Azure OpenAI ĐÚNG CHUẨN
client = AzureOpenAI(
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    api_key=os.getenv("AZURE_API_KEY")
)

# ✅ Khởi tạo agent LangGraph ReAct
def chat_completion(messages):
    response = client.chat.completions.create(
        messages=messages,
        max_tokens=4096,
        temperature=0.2,
        top_p=1.0,
        model=os.getenv("AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT")
    )
    return response

# Tạo agent_runnable sử dụng chat_completion
def agent_runnable(state):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": state["input"]}
    ]
    response =  chat_completion(messages)
    # ✅ Trích kết quả từ response
    ai_reply = response.choices[0].message.content

    # ✅ Trả ra dict có key "answer"
    return {"answer": ai_reply}

def embedding_creation(inputs):
    embedding_response = client.embeddings.create(
        input=inputs,
        model=os.getenv("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT")
    )
    return [item.embedding for item in embedding_response.data]

# ✅ Định nghĩa state schema
class AgentState(TypedDict):
    input: str
    answer: str

# ✅ Khởi tạo LangGraph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_runnable)
graph.set_entry_point("agent")
graph.set_finish_point("agent")
app = graph.compile()
