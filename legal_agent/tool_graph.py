# legal_agent/tool_graph.py
from langchain.tools import tool
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASS", "czech123"))
)

@tool
def search_graph_tool(query: str) -> str:
    """
    Truy vấn luật pháp Czech trong graph Neo4j.
    """
    cypher = """
    MATCH (c:Clause)
    WHERE toLower(c.clause_title) CONTAINS toLower($query)
       OR toLower(c.clause_content) CONTAINS toLower($query)
    RETURN c.clause_id AS id, c.clause_title AS title, c.clause_content AS content
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(cypher, query=query)
        results = []
        for r in result:
            results.append(f"§ {r['id']} - {r['title']}\n{r['content'][:300]}...")
        return "\n\n".join(results) if results else "Không tìm thấy điều luật liên quan."
