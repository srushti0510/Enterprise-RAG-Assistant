import streamlit as st
import requests
import uuid

API_BASE_URL = "http://backend:8000"

from services.feedback_db import init_feedback_db, save_feedback


DEBUG_MODE = False
init_feedback_db()

def get_unique_sources(results):
    sources = []

    if not results:
        return sources

    metadatas = results["metadatas"][0]

    seen = set()

    for metadata in metadatas:
        source = metadata.get("source", "Unknown Source")
        page = metadata.get("page", "N/A")

        key = (source, page)

        if key not in seen:
            seen.add(key)
            sources.append({
                "source": source,
                "page": page
            })

    return sources

st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("Enterprise Knowledge Assistant")
st.write("Upload multiple PDF/DOCX documents and ask questions across your knowledge base.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}


input_type = st.radio(
    "Choose Source",
    ["PDF/DOCX Files", "Website URL"]
)

uploaded_files = []
url_input = None

if input_type == "PDF/DOCX Files":
    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX files",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

else:
    url_input = st.text_input("Enter Website URL")

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_BASE_URL}/upload-file",
                    files=files
                )

                if response.status_code != 200:
                    st.error(response.text)
                    st.stop()

                data = response.json()
                chunks_count = data["chunks_stored"]

            st.session_state.uploaded_files.append(uploaded_file.name)

            if chunks_count == 0:
                st.info(f"{uploaded_file.name} has already been processed.")
            else:
                st.success(f"{uploaded_file.name} processed. Stored {chunks_count} chunks.")

if input_type == "Website URL":
    if st.button("Process Website URL"):
        if not url_input or not url_input.strip():
            st.warning("Please enter a website URL.")
        elif url_input in st.session_state.uploaded_files:
            st.info("This website URL has already been processed.")
        else:
            with st.spinner(f"Processing website: {url_input}..."):
                response = requests.post(
                    f"{API_BASE_URL}/upload-url",
                    json={
                        "url": url_input
                    }
                )

                data = response.json()
                chunks_count = data["chunks_stored"]

            st.session_state.uploaded_files.append(url_input)

            if chunks_count == 0:
                st.info("This website URL has already been processed.")
            else:
                st.success(f"Website processed. Stored {chunks_count} chunks.")

if st.session_state.uploaded_files:
    with st.expander("Knowledge Base Documents", expanded=False):
        for file_name in st.session_state.uploaded_files:
            st.write(f"• {file_name}")

st.divider()


st.subheader("Chat with your Knowledge Base")

if not st.session_state.chat_history and not st.session_state.current_chat:
    st.info("Ask a question about your uploaded documents to begin chatting.")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

if st.session_state.current_chat:
    with st.chat_message("user"):
        st.write(st.session_state.current_chat["question"])

    with st.chat_message("assistant"):
        st.write(st.session_state.current_chat["answer"])

        question_key = st.session_state.current_chat["question"]

        if st.session_state.feedback_given.get(question_key):
            st.success("✓ Feedback received")
        else:
            st.caption("Was this answer helpful?")

            col1, col2, col3 = st.columns([1, 1, 8])

            with col1:
                if st.button("👍", key="helpful_current"):
                    save_feedback(
                        st.session_state.current_chat["question"],
                        st.session_state.current_chat["answer"],
                        "Helpful"
                    )
                    st.session_state.feedback_given[question_key] = True
                    st.toast("Feedback saved.")
                    st.rerun()

            with col2:
                if st.button("👎", key="not_helpful_current"):
                    save_feedback(
                        st.session_state.current_chat["question"],
                        st.session_state.current_chat["answer"],
                        "Not Helpful"
                    )
                    st.session_state.feedback_given[question_key] = True
                    st.toast("Feedback saved.")
                    st.rerun()

question = st.chat_input("Ask a question about your uploaded documents...")

if question:
    if not st.session_state.uploaded_files:
        st.warning("Please upload and process at least one document first.")
    else:
        if st.session_state.current_chat is not None:
            st.session_state.chat_history.append(st.session_state.current_chat)

        with st.spinner("Searching knowledge base and generating answer..."):
            response = requests.post(
                f"{API_BASE_URL}/ask",
                json={
                    "question": question,
                    "sources": st.session_state.uploaded_files,
                    "session_id": st.session_state.session_id
                }
            )

            data = response.json()

            answer = data["answer"]

        st.session_state.current_chat = {
            "question": question,
            "answer": answer,
            "results": None
        }

        st.rerun()

with st.sidebar.expander("Analytics Dashboard", expanded=False):
    response = requests.get(f"{API_BASE_URL}/analytics")
    analytics = response.json()

    st.metric("Total Feedback", analytics["total_feedback"])
    st.metric("Helpful", analytics["helpful"])
    st.metric("Not Helpful", analytics["not_helpful"])

    if analytics["total_feedback"] > 0:
        helpful_percent = (
            analytics["helpful"] / analytics["total_feedback"]
        ) * 100

        st.metric("Helpful Rate", f"{helpful_percent:.1f}%")

    st.subheader("Recent Feedback")

    st.dataframe(
        analytics["recent_feedback"],
        width="stretch"
    )