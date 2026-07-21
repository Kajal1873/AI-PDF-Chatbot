# 📄 AI PDF Chatbot

An intelligent Retrieval-Augmented Generation (RAG) chatbot that allows users to upload one or more PDF documents and ask natural language questions about their content.

The chatbot combines semantic search, keyword search, query rewriting, and a Large Language Model (LLM) to provide accurate, context-aware answers with source citations.

---

## ✨ Features

- 📄 Upload multiple PDF files
- 💬 Chat with your PDFs
- 🔍 Semantic Search using FAISS
- 🔑 Keyword Search using BM25
- 🤝 Reciprocal Rank Fusion (RRF)
- 🧠 Query Rewriting for follow-up questions
- 📚 Source citations with page numbers
- ⚡ Streaming responses
- 💾 Cached vector indexes
- 🔒 Secure API keys using `.env`

---

## 🛠 Tech Stack

- Python
- Streamlit
- Groq API
- FAISS
- Sentence Transformers
- BM25 (rank-bm25)
- python-dotenv

---

## 📂 Project Structure

```
PDF_Chatbot/
│
├── model/
├── utils/
├── data/
├── indexes/
├── chunks/
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone <your-github-repository>
cd PDF_Chatbot
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```text
GROQ_API_KEY=your_api_key
```

### Run the application

```bash
python -m streamlit run streamlit_app.py
```

---

## 📌 Future Improvements

- OCR support for scanned PDFs
- Clickable citations
- Chat export
- Deployment
- User authentication

---

## 👨‍💻 Author

Kajal Pandey