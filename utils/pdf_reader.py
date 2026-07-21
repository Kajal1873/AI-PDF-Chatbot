import fitz


def read_pdf(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_num, page in enumerate(document):

        pages.append(
            {
                "page": page_num + 1,
                "text": page.get_text()
            }
        )

    return pages