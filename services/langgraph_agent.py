from typing import TypedDict, Optional, List

from langgraph.graph import StateGraph, END

from services.langchain_rag_pipeline import generate_langchain_answer


class AgentState(TypedDict):
    question: str
    sources: List[str]
    conversation_memory: Optional[list]
    intent: str
    answer: str
    results: dict


def route_intent(state: AgentState):
    question = state["question"].lower()

    if any(word in question for word in ["summarize", "summary", "brief"]):
        intent = "summarize"
    elif any(word in question for word in ["compare", "difference", "differences"]):
        intent = "compare"
    else:
        intent = "qa"

    state["intent"] = intent
    return state


def qa_node(state: AgentState):
    answer, results = generate_langchain_answer(
        question=state["question"],
        sources=state["sources"],
        conversation_memory=state["conversation_memory"]
    )

    state["answer"] = answer
    state["results"] = results
    return state


def summarize_node(state: AgentState):
    summary_question = f"Summarize the uploaded document(s). User request: {state['question']}"

    answer, results = generate_langchain_answer(
        question=summary_question,
        sources=state["sources"],
        conversation_memory=state["conversation_memory"]
    )

    state["answer"] = answer
    state["results"] = results
    return state


def compare_node(state: AgentState):
    compare_question = f"Compare the relevant information from the uploaded document(s). User request: {state['question']}"

    answer, results = generate_langchain_answer(
        question=compare_question,
        sources=state["sources"],
        conversation_memory=state["conversation_memory"]
    )

    state["answer"] = answer
    state["results"] = results
    return state


def decide_next_node(state: AgentState):
    if state["intent"] == "summarize":
        return "summarize"
    elif state["intent"] == "compare":
        return "compare"
    else:
        return "qa"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", route_intent)
    graph.add_node("qa", qa_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("compare", compare_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "qa": "qa",
            "summarize": "summarize",
            "compare": "compare"
        }
    )

    graph.add_edge("qa", END)
    graph.add_edge("summarize", END)
    graph.add_edge("compare", END)

    return graph.compile()


agent_graph = build_graph()


def run_langgraph_agent(question, sources=None, conversation_memory=None):
    result = agent_graph.invoke({
        "question": question,
        "sources": sources or [],
        "conversation_memory": conversation_memory,
        "intent": "",
        "answer": "",
        "results": {}
    })

    return result["answer"], result["results"], result["intent"]