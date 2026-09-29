from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import classifier, reasoning_agent, tool_executor, general_agent


def route_after_classifier(state: AgentState) -> str:
    """Route to math_agent pipeline or general_agent based on query type."""
    if state.get("query_type") == "math":
        return "reasoning_agent"
    return "general_agent"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classifier", classifier)
    graph.add_node("reasoning_agent", reasoning_agent)
    graph.add_node("math_agent", tool_executor)
    graph.add_node("general_agent", general_agent)

    graph.set_entry_point("classifier")

    graph.add_conditional_edges(
        "classifier",
        route_after_classifier,
        {"reasoning_agent": "reasoning_agent", "general_agent": "general_agent"},
    )

    graph.add_edge("reasoning_agent", "math_agent")
    graph.add_edge("math_agent", END)
    graph.add_edge("general_agent", END)

    return graph.compile()
