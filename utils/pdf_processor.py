from utils.pdf_reader import read_pdf
from utils.chunker import create_chunks


def process_pdf(pdf_path, pdf_name):

    pages = read_pdf(pdf_path)

    chunks = create_chunks(pages)

    for chunk in chunks:
        chunk["pdf"] = pdf_name

    return chunks