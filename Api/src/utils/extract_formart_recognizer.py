def extract_and_format_content_document(content_document):
    document_text = ""
    for page in content_document.pages:
        document_text += f"--- Page {page.page_number} ---\n"
        for line in page.lines:
            document_text += f"{line.content}\n"

    return document_text