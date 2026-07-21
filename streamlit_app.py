import streamlit as st
import os
import time


from utils.retriever import retrieve_chunks
from model.llm import ask_llm
from model.query_rewriter import rewrite_query
from utils.pdf_processor import process_pdf
from utils.cache_manager import load_or_create_pdf_cache
from utils.embeddings import create_embeddings
from utils.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    save_chunks,
    load_chunks
)
from utils.hybrid_search import create_bm25


st.set_page_config(
    page_title="PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Chatbot")

if st.sidebar.button("🗑️ New Chat"):
    st.session_state.messages = []
    st.rerun()

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)
st.sidebar.markdown("---")

top_k = st.sidebar.slider(
    "Top Chunks",
    min_value=1,
    max_value=20,
    value=10
)

if uploaded_files and (
    "index" not in st.session_state
    or st.session_state.get("uploaded_files") != [f.name for f in uploaded_files]
):

    os.makedirs("data", exist_ok=True)

    all_chunks = []

    for uploaded_file in uploaded_files:

        pdf_path = os.path.join("data", uploaded_file.name)

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        filename = uploaded_file.name.replace(".pdf", "").replace(" ", "_").lower()

        chunks = process_pdf(pdf_path, uploaded_file.name)

        index, chunks = load_or_create_pdf_cache(filename, chunks)

        all_chunks.extend(chunks)

    embeddings = create_embeddings(all_chunks)
    final_index = create_vector_store(embeddings)

    st.session_state.index = final_index
    st.session_state.bm25 = create_bm25(all_chunks)
    st.session_state.chunks = all_chunks
    st.session_state.uploaded_files = [f.name for f in uploaded_files]

    st.sidebar.success("PDF Ready!")
# Load vector store only once
if uploaded_files:

    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 Uploaded PDFs")

    for file in uploaded_files:
        st.sidebar.success(file.name)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "index" not in st.session_state:
    st.info("Upload a PDF to start chatting.")
    st.stop()

prompt = st.chat_input("Ask a question about your PDF")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching document..."):

            search_query = rewrite_query(
                prompt,
                st.session_state.messages
            )

            st.sidebar.write("Rewritten Query:", search_query)

            context, sources = retrieve_chunks(
                search_query,
                st.session_state.index,
                st.session_state.bm25,
                st.session_state.chunks,
                top_k
            )
            start = time.time()

            answer = ask_llm(
                prompt,
                context,
                st.session_state.messages
            )
            end = time.time()

            placeholder = st.empty()

            display_text = ""

            for word in answer.split():

                display_text += word + " "

                placeholder.markdown(display_text)

                time.sleep(0.03)

            st.caption(f"⏱️ Response Time: {(end-start):.2f} sec")

            st.markdown("---")

            with st.expander("📄 Retrieved Context"):
                st.write(context)

            st.markdown("### 📚 Sources")

            for source in sources:
                st.info(f"📄 **{source['pdf']}**  |  📖 Page {source['page']}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )