import fitz  # PyMuPDF

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    results = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if text:
                results.append({
                    "page": page_num,
                    "text": text
                })
    return results
