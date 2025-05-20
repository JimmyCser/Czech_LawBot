# import os
# from extract.extract_pdf import extract_text_blocks
# from extract.chunk_by_heading import parse_structure
# from extract.save_to_json import save_to_json
# from vector.embed import embed_clauses
# from db.neo4j_load import insert_all

# INPUT_DIR = "data"
# OUTPUT_DIR = "outputs"

# def process_file(file_path: str, output_json_path: str):
#     print(f"📄 Đang xử lý file: {file_path}")

#     # 1. Trích xuất PDF
#     blocks = extract_text_blocks(file_path)

#     # 2. Phân tích heading → clause
#     clauses = parse_structure(blocks)

#     # 3. Lưu ra JSON
#     save_to_json(clauses, output_json_path)

#     # 4. Nhúng vector
#     embedded_data = embed_clauses(output_json_path)

#     # 5. Insert vào Neo4j
#     insert_all(embedded_data)

#     print(f"✅ Hoàn tất: {file_path}")

# def main():
#     for fname in os.listdir(INPUT_DIR):
#         if fname.endswith(".pdf"):
#             pdf_path = os.path.join(INPUT_DIR, fname)
#             json_name = os.path.splitext(fname)[0] + ".json"
#             json_path = os.path.join(OUTPUT_DIR, json_name)

#             process_file(pdf_path, json_path)

# if __name__ == "__main__":
#     main()
