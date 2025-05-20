
# 🇨🇿 Czech Legal AI Agent – Assignment Demo

This project implements a smart retrieval-based AI agent for Czech law using LangGraph, Neo4j, and Azure OpenAI.

---

## 📦 Folder Structure

```
czech/
├── data/                      # Source PDF (e.g., CzechLaw.pdf)
├── db/                        # Neo4j loader
├── extract/                   # PDF extractor & chunker
├── vector/                    # Embedding logic
├── langgraph_app/             # LangGraph RAG pipeline (vector-based)
├── legal_agent/               # Tool-using agent with ReAct (graph-based)
├── outputs/                   # Intermediate files (JSON, etc.)
├── .env                       # Azure & Neo4j credentials
├── requirements.txt           # Dependencies
├── main.py                    # Full pipeline to extract → embed → load
└── test_query.py              # Run a sample agent query
```

---

## ✅ Features

- Extract structured sections (clauses) from Czech legislative PDF
- Insert content & metadata into **Neo4j** graph
- Compute embeddings using **Azure OpenAI**
- Use **LangGraph ReAct Agent** to intelligently answer legal questions
- Respond based on graph search results
- Ready to extend with vector / hybrid tools

---

## 🧪 Quick Start (Local Demo)



### 1. Set up Python environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

```env
AZURE_ENDPOINT=https://<your-endpoint>.openai.azure.com/
AZURE_API_KEY=sk-...
AZURE_API_VERSION=2024-12-01-preview

AZURE_OPENAI_CHAT_MODEL_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT=ace-text-embedding-3-large

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=#your neo4jDB password
```

---

## ⚙️ Build Full Pipeline

This command extracts → chunks → embeds → loads into Neo4j:

```bash
python main.py
```

---

## 💬 Run a Test Query via Agent

```bash
python -m legal_agent.test_query
```

You will see output like:

```
📌 Question
Which agency is responsible for trade licensing in Czech law?

🧠 Answer from bot:
In the Czech Republic, the agency responsible for trade licensing is...
```

---

## ✨ Notes

- Agent only uses **graph search** tool in this version (not vector/hybrid yet)
- LangGraph ReAct Agent determines tool use
- Graph contains clauses indexed by title/content

---

## 📍 Authors & Credits

- Assignment by: Mphuc
- Built with ❤️ using LangGraph, Neo4j, and Azure OpenAI
