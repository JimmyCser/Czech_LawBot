import re
from typing import List, Dict

def classify_line(line: str) -> str:
    """Nhận diện dòng là heading nào"""
    line = line.strip()
    if re.match(r"^ČÁST\s+[A-ZÍ]{2,}", line): return "part"
    if re.match(r"^HLAVA\s+[IVXLCDM]+", line): return "chapter"
    if re.match(r"^ODDÍL\s+\d+", line): return "section"
    if re.match(r"^§\s*\d+", line): return "clause"
    return "text"

def parse_structure(blocks: List[Dict]) -> List[Dict]:
    """Trích xuất cấu trúc phân cấp từ danh sách đoạn PDF"""
    clauses = []

    current_part = None
    current_chapter = None
    current_section = None
    current_clause = None

    for b in blocks:
        text = b["text"].strip()
        if not text: continue

        typ = classify_line(text)

        if typ == "part":
            current_part = text
        elif typ == "chapter":
            current_chapter = text
        elif typ == "section":
            current_section = text
        elif typ == "clause":
            # nếu có điều luật cũ đang xây dựng → lưu lại
            if current_clause:
                clauses.append(current_clause)

            current_clause = {
                "part": current_part,
                "chapter": current_chapter,
                "section": current_section,
                "clause_id": text,
                "clause_title": "",
                "clause_content": ""
            }
        else:
            # text thường → gán vào clause hiện tại
            if current_clause:
                if current_clause["clause_title"] == "":
                    current_clause["clause_title"] = text
                else:
                    current_clause["clause_content"] += " " + text
            else:
                # Không thuộc clause nào (văn bản đầu file?) → bỏ qua hoặc lưu vào log
                pass

    # Lưu clause cuối cùng
    if current_clause:
        clauses.append(current_clause)

    return clauses
