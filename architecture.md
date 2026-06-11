# Architecture

```mermaid
flowchart TD

A[PDF / DOCX / Website URL] --> B[FastAPI Backend]

B --> C[Document Loader]
C --> D[Text Chunking]
D --> E[OpenAI Embeddings]
E --> F[ChromaDB Vector Store]

F --> G[Hybrid Retrieval]
G --> H[Vector Search + Keyword Search]
H --> I[GPT-4o-mini]
I --> J[Answer with Sources]

K[Streamlit UI] --> B
J --> K

K --> L[User Feedback]
L --> M[SQLite Database]
M --> N[Analytics API]
N --> K

System Flow
User uploads a PDF/DOCX file or enters a website URL.
Streamlit sends the request to FastAPI.
FastAPI extracts document text using the document loader.
Text is split into chunks.
Chunks are embedded using OpenAI embeddings.
Embeddings and metadata are stored in ChromaDB.
User asks a question through Streamlit.
FastAPI performs hybrid retrieval using vector search and keyword search.
Retrieved context is passed to GPT-4o-mini.
The answer is returned to Streamlit.
User feedback is stored in SQLite.
Analytics are displayed in the dashboard.