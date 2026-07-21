                    User
                      │
                      ▼
               Streamlit UI
                      │
          Upload PDF / Ask Question
                      │
                      ▼
              Query Rewriter
                      │
                      ▼
          PDF Chunk Retrieval
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
     FAISS Search             BM25 Search
          │                         │
          └────────────┬────────────┘
                       ▼
          Reciprocal Rank Fusion
                       ▼
             Retrieved Chunks
                       ▼
                 Groq LLM
                       ▼
              Final AI Response
                       ▼
          Source Citations + Chat