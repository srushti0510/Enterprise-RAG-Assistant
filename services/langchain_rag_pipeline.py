from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from services.vector_store import hybrid_search


def format_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, doc in enumerate(documents, start=1):
        metadata = metadatas[i - 1]
        source = metadata.get("source", "Unknown Source")
        page = metadata.get("page", "N/A")

        context_parts.append(
            f"Source chunk {i}\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{doc}"
        )

    return "\n\n---\n\n".join(context_parts)


def format_conversation_memory(conversation_memory):
    if not conversation_memory:
        return "No previous conversation."

    if isinstance(conversation_memory, str):
        return conversation_memory

    memory_parts = []

    for turn in conversation_memory:
        if isinstance(turn, dict):
            question = turn.get("question", "")
            answer = turn.get("answer", "")

            memory_parts.append(
                f"User: {question}\n"
                f"Assistant: {answer}"
            )
        else:
            memory_parts.append(str(turn))

    return "\n\n".join(memory_parts)


def generate_langchain_answer(question, sources=None, conversation_memory=None):
    results = hybrid_search(
        query=question,
        sources=sources,
        n_results=8
    )

    context = format_context(results)
    memory = format_conversation_memory(conversation_memory)

    prompt = ChatPromptTemplate.from_template("""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided document context.

Use conversation memory only to understand follow-up questions.
Do not use conversation memory as factual evidence unless it is supported by the document context.

If the answer is not present in the document context, say:
"I could not find enough information in the uploaded documents."

Conversation memory:
{memory}

Document context:
{context}

Question:
{question}

Answer:
""")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "memory": memory,
        "context": context,
        "question": question
    })

    return answer, results