from pypdf import PdfReader

reader = PdfReader("financial_knowledge_base.pdf")

page_extract = reader.pages[0:4]

pages_list = []
pages_id = []
for page in page_extract:
    pages_id.append(f"page_{len(pages_id) + 1}")
    pages_list.append(page.extract_text())
