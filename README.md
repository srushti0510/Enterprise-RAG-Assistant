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
- LangChain Prompt Templates
- LangChain Output Parsing
- LangGraph Agent Workflow
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

- Built an Agentic Retrieval-Augmented Generation (RAG) system using LangChain, LangGraph, OpenAI, ChromaDB, FastAPI, and Streamlit
- Developed LangGraph-based workflow routing for question answering, document summarization, and comparison tasks
- Implemented hybrid retrieval combining semantic search and keyword matching
- Added support for PDF, DOCX, and Website URL ingestion
- Developed chat-style conversation memory for follow-up questions
- Built analytics dashboard with SQLite-backed feedback tracking
- Containerized the entire application using Docker and Docker Compose
- Designed a modular backend architecture for scalability and maintainability

---

## Evaluation Framework

To measure retrieval and answer quality, the project includes an automated evaluation framework.

### Components

- Benchmark evaluation dataset
- Automated question execution
- Expected answer validation
- Pass/Fail scoring
- Retrieval regression testing

### Running Evaluations

```bash
python evals/run_evals.py
```
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

### Why LangChain?

LangChain was added to structure the RAG pipeline around reusable prompt templates, LLM orchestration, and output parsing.

Instead of manually building prompts and directly calling the OpenAI API, LangChain provides a cleaner abstraction for:

- Prompt template management
- LLM invocation
- Output parsing
- Chain composition

Benefits:

- Cleaner and more maintainable RAG pipeline
- Easier prompt iteration
- Better separation between retrieval, prompting, and answer generation
- Easier future integration with tools, agents, and evaluators
---

### Why LangGraph?

Traditional RAG systems follow a single retrieval and answer generation path.

LangGraph was introduced to enable agentic workflows where the system can route user requests to specialized execution paths such as:

- Question Answering
- Document Summarization
- Document Comparison

Benefits:

- More flexible task handling
- Cleaner workflow orchestration
- Easier future expansion into tool-using agents

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
├── app.py
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── services/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── url_loader.py
│   ├── vector_store.py
│   ├── rag_pipeline.py
│   ├── conversation_memory.py
│   ├── feedback_db.py
│   ├── analytics.py
│   ├── langgraph_agent.py
│   └── langchain_rag_pipeline.py
│ 
├── data/
│   └── sample_doc.docx
│
├── evals/
│   ├── eval_questions.json
│   └── run_evals.py
│
├── chroma_db/
│
├── Dockerfile
├── docker-compose.yml
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
2. FastAPI processes and extracts the content.
3. Text is chunked and converted into embeddings.
4. Embeddings are stored in ChromaDB.
5. User submits a query through the Streamlit interface.
6. Hybrid retrieval performs:
   - Semantic Vector Search
   - Keyword Search
7. LangGraph routes the request to the appropriate workflow:
   - Question Answering
   - Document Summarization
   - Document Comparison
8. LangChain constructs the prompt and orchestrates the LLM call.
9. GPT-4o-mini generates a grounded response using retrieved context.
10. Conversation memory is used to support follow-up questions.
11. User feedback is stored in SQLite.
12. Analytics dashboard tracks feedback and usage metrics.

---

## Example Evaluation

### Document

sample_doc.docx

### Question

```text
How many days per week can employees work remotely?
```

### Answer

```text
Employees may work remotely up to 3 days per week with manager approval.
```

### Source

```text
sample_doc.docx – Page 1
```

This demonstrates grounded retrieval, source attribution, and natural language question answering over uploaded documents.

---

## Evaluation Results

The automated evaluation framework was tested using benchmark enterprise-policy questions.

```text
Evaluation Results: 3/3 Passed
```

The evaluation verifies:

- Retrieval accuracy
- Context grounding
- Answer correctness
- Source attribution

---

## Future Roadmap

- Tool-using Agents
- Web Search Integration
- Multi-Agent Collaboration
- Automated RAG Evaluation
- User Authentication
- Role-Based Access Control
- Citation Highlighting
- Multi-Tenant Knowledge Bases
- Redis Caching
- PostgreSQL Analytics Storage
- Cloud Deployment (AWS/Azure/GCP)

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