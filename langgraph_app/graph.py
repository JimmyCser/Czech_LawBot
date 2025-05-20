from langgraph.graph import StateGraph
from openai import AzureOpenAI
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import numpy as np
from typing import TypedDict

# Load env
load_dotenv()

# Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)

# Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "czech123"))

# Cosine similarity thuần Python
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Tạo embedding từ câu hỏi
def get_question_embedding(question: str) -> list:
    res = client.embeddings.create(
        input=[question],
        model=os.getenv("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT")
    )
    return res.data[0].embedding

# Truy vấn Neo4j → tính cosine tại client
def get_similar_clauses(question: str, top_k=5) -> list:
    q_vector = get_question_embedding(question)
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Clause)
            WHERE c.embedding IS NOT NULL
            RETURN c.clause_id AS id, c.clause_title AS title, c.clause_content AS content, c.embedding AS embedding
        """)
        scored = []
        for record in result:
            emb = record["embedding"]
            score = cosine_similarity(q_vector, emb)
            scored.append({
                "id": record["id"],
                "title": record["title"],
                "content": record["content"],
                "score": score
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

# Tạo context và trả lời
def answer_query(state):
    question = state["input"]
    context_clauses = get_similar_clauses(question, top_k=5)

    # Lọc clause trùng
    unique = {}
    for c in context_clauses:
        if c["id"] not in unique:
            unique[c["id"]] = c
    context_clauses = list(unique.values())

    # Ghép context
    context_text = ""
    for c in context_clauses:
        context_text += f"{c['id']} - {c['title']}\n{c['content']}\n\n"

    # Prompt chuẩn
    system_prompt = (
        "You are a legal assistant specialized in Czech law.\n"
        "Use the following legal clauses to answer the question.\n"
        "Return your answer in clear Markdown bullet points. Do not repeat the same clause multiple times.\n"
        "Use § numbers if relevant. Only use information found in the context.\n"
        "Do not invent information.\n\n"
        f"---\n{context_text}---"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    # Gọi GPT và stream
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT"),
        messages=messages,
        temperature=0.2,
        stream=True
    )

    # Thu stream an toàn
    answer_chunks = []
    for chunk in response:
        try:
            content_piece = chunk.choices[0].delta.content
            if content_piece:
                answer_chunks.append(content_piece)
        except (AttributeError, IndexError):
            continue
    final_answer = "".join(answer_chunks)

    # ✅ RETURN CHUẨN!
    return {
        "answer": final_answer,
        "context_used": context_clauses
    }

# LangGraph setup
class GraphState(TypedDict, total=False):
    input: str
    answer: str
    context_used: list

graph = StateGraph(GraphState)
graph.add_node("query", answer_query)
graph.set_entry_point("query")
app = graph.compile()
