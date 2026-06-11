# Enterprise Knowledge Assistant

An enterprise-grade Retrieval-Augmented Generation (RAG) application that enables users to upload PDF/DOCX documents or ingest website URLs, ask natural language questions, and receive context-aware answers powered by OpenAI and ChromaDB.

The application follows a modular, production-inspired architecture featuring a FastAPI backend, Streamlit frontend, hybrid retrieval pipeline, vector database, conversation memory, and analytics dashboard.

---

## Features

### Multi-Source Knowledge Ingestion

- PDF document upload
- DOCX document upload
- Website URL ingestion
- Automatic text extraction and chunking

### Retrieval-Augmented Generation (RAG)

- OpenAI Embeddings (`text-embedding-3-small`)
- ChromaDB vector database
- Hybrid Retrieval
  - Semantic Vector Search
  - Keyword Search
- GPT-4o-mini answer generation

### Enterprise Features

- FastAPI backend APIs
- Streamlit frontend
- Chat-style interface
- Conversation memory
- Source-aware responses
- Source citations
- Duplicate document detection
- Feedback collection
- Analytics dashboard
- SQLite feedback storage
- Dockerized deployment

---
## Key Highlights

- Built an end-to-end RAG system using OpenAI, ChromaDB, FastAPI, and Streamlit
- Implemented hybrid retrieval combining semantic search and keyword matching
- Added support for PDF, DOCX, and Website URL ingestion
- Developed chat-style conversation memory for follow-up questions
- Built analytics dashboard with SQLite-backed feedback tracking
- Containerized the entire application using Docker and Docker Compose
- Designed a modular backend architecture for scalability and maintainability

---

## Architecture

See [architecture.md](architecture.md) for the complete system architecture and workflow.

---

## Tech Stack

### Frontend

- Streamlit

### Backend

- FastAPI

### LLM & AI

- OpenAI GPT-4o-mini
- OpenAI Embeddings

### Vector Database

- ChromaDB

### Data Processing

- PyPDF
- Python-Docx
- BeautifulSoup4
- Requests

### Storage

- SQLite
- ChromaDB Persistent Storage

---

## Technical Decisions & Tradeoffs

### Why ChromaDB?

ChromaDB was selected because it is lightweight, open-source, and easy to run locally without additional infrastructure.

Tradeoff:
- Simpler local development
- Less operational overhead

Alternative considered:
- Pinecone (managed cloud vector database)

For production-scale deployments, Pinecone or Weaviate could be used.

---

### Why FastAPI + Streamlit?

FastAPI handles API orchestration and backend processing while Streamlit provides a rapid UI for interacting with the knowledge base.

Benefits:
- Clear separation of frontend and backend concerns
- Easier deployment and testing
- Better scalability compared to a single-script architecture

---

### Why Hybrid Retrieval?

Pure vector search can miss exact keyword matches.

Hybrid retrieval combines:

- Semantic similarity search
- Keyword-based matching

Benefits:
- Improved answer relevance
- Better handling of technical terminology
- Reduced retrieval failures

---

### Why Docker?

Docker ensures consistent execution across environments by packaging:

- Python runtime
- Dependencies
- Application code

Benefits:
- Reproducible builds
- Easier onboarding
- Simplified deployment

---

### Why SQLite for Feedback Analytics?

SQLite was selected because it is lightweight and sufficient for storing user feedback and analytics during development.

For production systems, PostgreSQL would be preferred.

---

## Project Structure

```text
Enterprise-RAG-Assistant/
│
├── app.py                         # Streamlit frontend
│
├── backend/
│   ├── __init__.py
│   └── main.py                    # FastAPI backend APIs
│
├── services/
│   ├── __init__.py
│   ├── document_loader.py         # PDF/DOCX ingestion
│   ├── url_loader.py              # Website content ingestion
│   ├── vector_store.py            # ChromaDB + embeddings
│   ├── rag_pipeline.py            # Retrieval + answer generation
│   ├── conversation_memory.py     # Session conversation history
│   ├── feedback_db.py             # Feedback persistence
│   └── analytics.py               # Analytics dashboard logic
│
├── chroma_db/                     # Persistent vector database
│
├── Dockerfile                     # Application container
├── docker-compose.yml             # Multi-container deployment
├── .gitignore
├── .dockerignore
│
├── architecture.md
├── README.md
└── requirements.txt
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Upload PDF/DOCX

```http
POST /upload-file
```

### Upload Website URL

```http
POST /upload-url
```

### Ask Questions

```http
POST /ask
```

### Analytics

```http
GET /analytics
```

### Debug Sources

```http
GET /debug/sources
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Enterprise-RAG-Assistant
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Docker Setup

Build and run the application:

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:8501
```

Backend API:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

The Docker Compose configuration runs:

- Streamlit Frontend
- FastAPI Backend

as separate services.

---

## Running the Application

### Start FastAPI Backend

```bash
python -m uvicorn backend.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit Frontend

```bash
streamlit run app.py
```

---

## Example Workflow

1. Upload a PDF/DOCX document or enter a website URL.
2. FastAPI processes the content.
3. Text is chunked and embedded.
4. Embeddings are stored in ChromaDB.
5. Ask questions through the Streamlit interface.
6. Hybrid retrieval fetches relevant context.
7. GPT-4o-mini generates answers.
8. User feedback is stored in SQLite.
9. Analytics dashboard displays usage metrics.

---

## Example Evaluation

### Document

Loan_Sanction_Letter.pdf

### Question

```text
What is the repayment period?
```

### Answer

```text
The repayment period is 180 months after the completion of the moratorium period.
```

### Source

```text
Loan_Sanction_Letter.pdf – Page 1
```

This demonstrates grounded retrieval and source attribution.

## Future Roadmap

- Retrieval evaluation framework
- Reranking models
- User Authentication
- Role-Based Access Control
- Citation Highlighting
- Multi-Tenant Knowledge Bases
- Redis Caching

---


## Sample Use Cases

- Enterprise Knowledge Management
- Internal Policy Search
- Loan and Financial Document Analysis
- Contract and Agreement Review
- Research Assistant for Websites and Reports
- Employee Self-Service Knowledge Base

---

## License

This project is intended for educational, portfolio, and learning purposes.