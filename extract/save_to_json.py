import json
from typing import List, Dict

def save_to_json(clauses: List[Dict], output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clauses, f, ensure_ascii=False, indent=2)
