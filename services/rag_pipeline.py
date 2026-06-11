from openai import OpenAI
from dotenv import load_dotenv
from services.vector_store import hybrid_search

load_dotenv()

openai_client = OpenAI()


def build_context(results):
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = ""

    for i, document in enumerate(documents):
        source = metadatas[i]["source"]
        page = metadatas[i].get("page", "N/A")
        chunk = metadatas[i]["chunk"]

        context += f"\nSource: {source}, Page: {page}, Chunk: {chunk}\n"
        context += document
        context += "\n"

    return context



def generate_answer(question: str, sources=None, conversation_memory: str = ""):
    results = hybrid_search(
        query=question,
        sources=sources,
        n_results=15
    )

    context = build_context(results)

    prompt = f"""
    You are an enterprise knowledge assistant.

    Use only the retrieved document context below to answer the question.

    You may use the recent conversation memory only to understand follow-up questions,
    references like "it", "this", "that", or previous topics.
    Do not use conversation memory as factual evidence unless the same fact is supported
    by the retrieved document context.

    Rules:
    1. Answer only from the provided document context.
    2. Use conversation memory only for understanding the user's intent.
    3. The context may come from PDF forms, tables, invoices, contracts, or applications where formatting may be lost during extraction.
    4. When labels and values appear close together, infer the correct label-value relationship carefully.
    5. Use nearby fields, headings, signatures, names, and form structure to determine answers.
    6. If multiple possible values exist, choose the one most strongly associated with the requested field.
    7. Users may use different words than the document. For example, applicant, requestor, petitioner, signer, borrower, customer, and person filing may refer to related people depending on the document.
    8. If the answer is not present in the retrieved document context, say: "I could not find this information in the uploaded documents."
    9. Keep the answer concise.
    10. Always cite the source and page number.

    Recent Conversation Memory:
    {conversation_memory if conversation_memory else "No previous conversation."}

    Retrieved Document Context:
    {context}

    Current Question:
    {question}
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You answer questions using only uploaded enterprise documents. Use conversation memory only to understand follow-up questions, not as factual evidence."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content, results