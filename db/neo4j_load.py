from neo4j import GraphDatabase
from typing import List, Dict

# ⚠️ Update password Neo4j 
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "czech123"  

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def insert_clause(tx, clause: Dict):
    tx.run(
        """
        MERGE (c:Clause {clause_id: $id})
        SET c.clause_title = $title,
            c.clause_content = $content,
            c.part = $part,
            c.chapter = $chapter,
            c.section = $section,
            c.embedding = $embedding
        """,
        id=clause["clause_id"],
        title=clause["clause_title"],
        content=clause["clause_content"],
        part=clause.get("part", ""),
        chapter=clause.get("chapter", ""),
        section=clause.get("section", ""),
        embedding=clause["embedding"]
    )

def insert_all(clauses: List[Dict]):
    with driver.session() as session:
        for clause in clauses:
            try:
                session.execute_write(insert_clause, clause)
            except Exception as e:
                print(f"❌ Lỗi khi insert {clause['clause_id']}: {e}")
