# Architecture

```mermaid
flowchart TD

U[User]

U --> S[Streamlit Frontend]

S --> F[FastAPI Backend]

F --> DL[Document Loader]
DL --> TC[Text Chunking]
TC --> EMB[OpenAI Embeddings]
EMB --> VS[ChromaDB Vector Store]

S --> Q[User Question]
Q --> F

F --> HR[Hybrid Retrieval]
HR --> VS[Vector Search]
HR --> KS[Keyword Search]

VS --> GPT[GPT-4o-mini]
KS --> GPT

GPT --> A[Generated Answer]
A --> S

S --> FB[User Feedback]
FB --> SQL[SQLite Database]

SQL --> AN[Analytics Dashboard]
AN --> S
```

## Deployment Architecture

```text
                ┌─────────────────┐
                │      User       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Streamlit UI    │
                │ Docker Service  │
                └────────┬────────┘
                         │ HTTP
                         ▼
                ┌─────────────────┐
                │ FastAPI Backend │
                │ Docker Service  │
                └─────┬─────┬─────┘
                      │     │
          ┌───────────┘     └───────────┐
          ▼                             ▼
   ┌─────────────┐               ┌─────────────┐
   │ ChromaDB    │               │ SQLite      │
   │ Vector DB   │               │ Analytics   │
   └─────────────┘               └─────────────┘
                 \
                  \
                   ▼
            ┌─────────────┐
            │ OpenAI API  │
            └─────────────┘
```

## System Flow

1. User uploads a PDF/DOCX file or enters a website URL.
2. Streamlit sends the request to FastAPI.
3. FastAPI extracts document text using the document loader.
4. Text is split into chunks.
5. Chunks are embedded using OpenAI embeddings.
6. Embeddings and metadata are stored in ChromaDB.
7. User asks a question through Streamlit.
8. FastAPI performs hybrid retrieval using vector search and keyword search.
9. Retrieved context is passed to GPT-4o-mini.
10. The answer is returned to Streamlit.
11. User feedback is stored in SQLite.
12. Analytics are displayed in the dashboard.