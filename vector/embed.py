from openai import AzureOpenAI
from dotenv import load_dotenv
import os, json
from typing import List, Dict
import tiktoken
import numpy as np
import time

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)

# Tokenizer cho embedding model
encoder = tiktoken.encoding_for_model("text-embedding-3-large")
MAX_TOKENS = 8000  # an toàn hơn giới hạn 8192

def split_text(text: str, max_tokens: int) -> List[str]:
    words = text.split()
    chunks, current_chunk = [], []
    token_count = 0

    for word in words:
        word_tokens = len(encoder.encode(word))
        if token_count + word_tokens > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            token_count = word_tokens
        else:
            current_chunk.append(word)
            token_count += word_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        input=[text],
        model=os.getenv("AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT")
    )
    return response.data[0].embedding

def embed_clauses(json_path: str) -> List[Dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"🔎 Embedding {len(data)} clauses (handle long ones)...")

    for i, clause in enumerate(data):
        try:
            full_text = f"{clause['clause_id']} {clause['clause_title']}. {clause['clause_content']}"
            token_len = len(encoder.encode(full_text))

            if token_len > MAX_TOKENS:
                print(f"⚠️ Clause {clause['clause_id']} quá dài ({token_len} tokens) → CHUNK")
                chunks = split_text(full_text, max_tokens=MAX_TOKENS // 2)
                embeddings = [get_embedding(chunk) for chunk in chunks]
                final_embedding = list(np.mean(embeddings, axis=0))
            else:
                final_embedding = get_embedding(full_text)

            clause["embedding"] = final_embedding
            print(f"✅ Embedded {clause['clause_id']} ({i+1}/{len(data)})")
            time.sleep(0.2)

        except Exception as e:
            print(f"❌ Lỗi embedding tại {clause.get('clause_id', 'N/A')}: {e}")
            clause["embedding"] = []

    return data
