from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    all_chunks = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            all_chunks.append(
                {
                    "page": page["page"],
                    "text": chunk
                }
            )

    return all_chunks