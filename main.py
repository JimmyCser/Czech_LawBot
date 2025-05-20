from extract.extract_pdf import extract_text_blocks
from extract.chunk_by_heading import parse_structure
from extract.save_to_json import save_to_json
from vector.embed import embed_clauses
from db.neo4j_load import insert_all

def main():
    # Bước 1: Đọc PDF
    print("📄 Đang trích xuất từ CzechLaw.pdf...")
    blocks = extract_text_blocks("data/CzechLaw.pdf")

    # Bước 2: Tách heading, clause
    print("🧱 Đang phân tích cấu trúc heading...")
    clauses = parse_structure(blocks)

    # Bước 3: Lưu ra JSON (chưa embed)
    print("💾 Đang lưu JSON gốc...")
    save_to_json(clauses, "outputs/law_sections.json")

    # Bước 4: Tạo embedding
    print("🧠 Đang tạo embedding vector...")
    data_with_embedding = embed_clauses("outputs/law_sections.json")

    # Bước 5: Đẩy vào Neo4j
    print("📊 Đang insert vào Neo4j...")
    insert_all(data_with_embedding)

    print("✅ Toàn bộ pipeline đã hoàn tất!")

if __name__ == "__main__":
    main()
