from langgraph.graph import StateGraph, END

from .state import SupervisorWorkerState
from .nodes import supervisor, math_agent, leaves_balance, general_agent


def route(state: SupervisorWorkerState):
    return state["worker"]


def build_graph():

    graph = StateGraph(SupervisorWorkerState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("math_agent", math_agent)
    graph.add_node("leaves_balance", leaves_balance)
    graph.add_node("general_agent", general_agent)
    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route,
        {
            "math": "math_agent",
            "leave": "leaves_balance",
            "general": "general_agent",
        }
    )

    graph.add_edge("math_agent", END)
    graph.add_edge("leaves_balance", END)
    graph.add_edge("general_agent", END)

    return graph.compile()