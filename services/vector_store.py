import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="enterprise_documents"
)


def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)


def create_embedding(text: str):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def store_document(pages, source: str):
    existing_docs = collection.get(where={"source": source})

    if existing_docs["ids"]:
        return 0

    total_chunks = 0

    for page_data in pages:
        page_text = page_data["text"]
        page_number = page_data["page"]

        chunks = chunk_text(page_text)

        for index, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            chunk_id = f"{source}_page_{page_number}_chunk_{index}"

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": source,
                    "page": page_number if page_number else "N/A",
                    "chunk": index
                }]
            )

            total_chunks += 1

    return total_chunks


def search_documents(query: str, sources=None, n_results: int = 5):
    query_embedding = create_embedding(query)

    where_filter = None

    if sources:
        where_filter = {"source": {"$in": sources}}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter
    )

    return results

def keyword_search(query: str, sources=None):
    all_docs = collection.get()

    matched_docs = []
    matched_metadata = []

    query_words = query.lower().split()

    documents = all_docs["documents"]
    metadatas = all_docs["metadatas"]

    for doc, metadata in zip(documents, metadatas):

        if sources:
            if metadata["source"] not in sources:
                continue

        doc_lower = doc.lower()

        if any(word in doc_lower for word in query_words):
            matched_docs.append(doc)
            matched_metadata.append(metadata)

    return {
        "documents": [matched_docs[:5]],
        "metadatas": [matched_metadata[:5]]
    }

def hybrid_search(query: str, sources=None, n_results=8):

    vector_results = search_documents(
        query=query,
        sources=sources,
        n_results=n_results
    )

    keyword_results = keyword_search(
        query=query,
        sources=sources
    )

    combined_docs = []
    combined_metadata = []

    seen = set()

    for docs, metas in [
        (
            vector_results["documents"][0],
            vector_results["metadatas"][0]
        ),
        (
            keyword_results["documents"][0],
            keyword_results["metadatas"][0]
        )
    ]:

        for doc, meta in zip(docs, metas):

            key = (
                meta["source"],
                meta["chunk"]
            )

            if key not in seen:
                seen.add(key)

                combined_docs.append(doc)
                combined_metadata.append(meta)

    return {
        "documents": [combined_docs],
        "metadatas": [combined_metadata]
    }