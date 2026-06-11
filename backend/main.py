from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from services.rag_pipeline import generate_answer
from services.vector_store import collection, store_document
from services.document_loader import load_source
from services.analytics import get_feedback_summary
from services.feedback_db import init_feedback_db
from services.conversation_memory import (
    init_conversation_db,
    get_recent_conversation,
    save_conversation_turn
)


app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    version="1.0.0"
)


init_feedback_db()
init_conversation_db()


class AskRequest(BaseModel):
    question: str
    sources: list[str] = []
    session_id: str = "default"


class URLUploadRequest(BaseModel):
    url: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Enterprise Knowledge Assistant API is running"
    }


@app.post("/upload-url")
def upload_url(request: URLUploadRequest):
    pages = load_source(request.url, "url")

    chunks_count = store_document(
        pages,
        source=request.url
    )

    return {
        "status": "success",
        "source": request.url,
        "chunks_stored": chunks_count
    }

@app.post("/upload-file")
def upload_file(file: UploadFile = File(...)):

    file_extension = file.filename.lower().split(".")[-1]

    if file_extension not in ["pdf", "docx"]:
        return {
            "status": "error",
            "message": "Only PDF and DOCX files are supported."
        }

    pages = load_source(file.file, file_extension)

    chunks_count = store_document(
        pages,
        source=file.filename
    )

    return {
        "status": "success",
        "source": file.filename,
        "chunks_stored": chunks_count
    }

@app.post("/ask")
def ask_question(request: AskRequest):
    conversation_memory = get_recent_conversation(
        session_id=request.session_id,
        limit=5
    )

    answer, results = generate_answer(
        question=request.question,
        sources=request.sources,
        conversation_memory=conversation_memory
    )

    source_label = ", ".join(request.sources) if request.sources else "all_sources"

    save_conversation_turn(
        session_id=request.session_id,
        source=source_label,
        question=request.question,
        answer=answer
    )

    return {
        "answer": answer,
        "sources_used": len(results["documents"][0]),
        "memory_used": bool(conversation_memory)
    }


@app.get("/debug/sources")
def debug_sources():
    data = collection.get()

    sources = []

    for metadata in data["metadatas"]:
        source = metadata.get("source", "Unknown")
        if source not in sources:
            sources.append(source)

    return {
        "total_chunks": len(data["ids"]),
        "sources": sources
    }

@app.get("/analytics")
def analytics():
    data = get_feedback_summary()

    helpful_rate = 0

    if data["total"] > 0:
        helpful_rate = round(
            (int(data["helpful"]) / int(data["total"])) * 100,
            2
        )

    recent_feedback = data["recent"]

    if hasattr(recent_feedback, "to_dict"):
        recent_feedback = recent_feedback.to_dict(orient="records")

    return {
        "total_feedback": int(data["total"]),
        "helpful": int(data["helpful"]),
        "not_helpful": int(data["not_helpful"]),
        "helpful_rate": helpful_rate,
        "recent_feedback": recent_feedback
    }