"""Streamlit frontend for the agentic AI design patterns demo."""

import streamlit as st

from patterns.planner_executor.graph import build_graph as build_planner_executor_graph
from patterns.supervisor_worker.graph import build_graph as build_supervisor_worker_graph
from patterns.tool_using.graph import build_graph as build_tool_using_graph


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Agentic AI Pattern Demo",
    page_icon="🤖",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "tool_graph" not in st.session_state:
    st.session_state.tool_graph = build_tool_using_graph()

if "planner_graph" not in st.session_state:
    st.session_state.planner_graph = build_planner_executor_graph()

if "supervisor_graph" not in st.session_state:
    st.session_state.supervisor_graph = build_supervisor_worker_graph()

if "tool_messages" not in st.session_state:
    st.session_state.tool_messages = []

if "planner_messages" not in st.session_state:
    st.session_state.planner_messages = []

if "supervisor_messages" not in st.session_state:
    st.session_state.supervisor_messages = []


# ---------------------------------------------------------------------------
# Demo renderers
# ---------------------------------------------------------------------------
def render_tool_using_demo():
    st.title("🤖 Tool-Using Agentic AI Workflow")
    st.markdown(
        """
        This workflow uses **two specialised agents** behind the scenes:

        1. **Classifier** – decides whether your question is *math* or *general*.
        2. **Reasoning Agent** – converts math questions into Python expressions.
        3. **Math Agent** – evaluates the expression safely.
        4. **General Agent** – answers general questions using an LLM.

        ---
        """
    )

    for msg in st.session_state.tool_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "details" in msg:
                with st.expander("🔍 Workflow details"):
                    st.json(msg["details"])

    if prompt := st.chat_input("Ask a math question or anything else…", key="tool_input"):
        st.session_state.tool_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                result = st.session_state.tool_graph.invoke({"question": prompt})

            query_type = result.get("query_type", "unknown")

            if query_type == "math":
                expression = result.get("expression", "")
                answer = result.get("result", "")
                st.markdown(f"**Answer:** {answer}")
                with st.expander("🔍 Workflow details"):
                    st.json(
                        {
                            "Query Type": "Math",
                            "Expression": expression,
                            "Result": answer,
                        }
                    )
                st.session_state.tool_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "details": {
                            "Query Type": "Math",
                            "Expression": expression,
                            "Result": answer,
                        },
                    }
                )
            else:
                answer = result.get("answer", "")
                st.markdown(f"**Answer:** {answer}")
                with st.expander("🔍 Workflow details"):
                    st.json({"Query Type": "General", "Answer": answer})
                st.session_state.tool_messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "details": {"Query Type": "General", "Answer": answer},
                    }
                )

    with st.sidebar:
        st.header("💡 Tool-Using examples")
        st.markdown(
            """
            **Math questions:**
            - What is 15 + 27?
            - What is the average of 100 and 200?
            - Compute (12 + 8) * 5
            - What is the square of 9?

            **General questions:**
            - Define AI
            - What is machine learning?
            - Explain the theory of relativity
            - Who wrote Romeo and Juliet?
            """
        )
        if st.button("🗑️ Clear tool chat", key="clear_tool_chat"):
            st.session_state.tool_messages = []
            st.rerun()


def render_planner_executor_demo():
    st.title("🧠 Planner-Executor Agentic AI Workflow")
    st.markdown(
        """
        This workflow follows a **manager → worker** pattern:

        1. **Planner** breaks the task into a short action plan.
        2. **Executor** takes each step and produces the final answer.

        The system is designed for tasks that need a clear step-by-step response.

        ---
        """
    )

    for msg in st.session_state.planner_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "details" in msg:
                with st.expander("🔍 Workflow details"):
                    st.json(msg["details"])

    if prompt := st.chat_input(
        "Describe a task to plan and execute…",
        key="planner_input",
    ):
        st.session_state.planner_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Planning and executing…"):
                result = st.session_state.planner_graph.invoke({"task": prompt})

            plan = [step.strip() for step in result.get("plan", []) if str(step).strip()]
            output = result.get("output", "")

            st.markdown("### Plan")
            for step in plan:
                st.markdown(f"- {step.lstrip('-').strip()}")

            st.markdown("### Execution result")
            st.markdown(output)

            with st.expander("🔍 Workflow details"):
                st.json({"Task": prompt, "Plan": plan, "Output": output})

            st.session_state.planner_messages.append(
                {
                    "role": "assistant",
                    "content": output,
                    "details": {
                        "Task": prompt,
                        "Plan": plan,
                        "Output": output,
                    },
                }
            )

    with st.sidebar:
        st.header("💡 Planner-Executor examples")
        st.markdown(
            """
            - Create a 3-step plan for launching a chatbot product.
            - Plan how to organize a weekend study schedule.
            - Break down the steps to write a technical blog post.
            - Create a plan for launching a new AI startup.
            """
        )
        if st.button("🗑️ Clear planner chat", key="clear_planner_chat"):
            st.session_state.planner_messages = []
            st.rerun()


def render_supervisor_worker_demo():
    st.title("👥 Supervisor-Worker Agentic AI Workflow")
    st.markdown(
        """
        This workflow uses a **supervisor** to route requests to the right specialist worker.

        - **Supervisor** decides whether the request is *math* or *leave*.
        - **Math agent** solves arithmetic and numeric questions.
        - **Leave agent** checks employee leave balances from a database.

        ---
        """
    )

    for msg in st.session_state.supervisor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "details" in msg:
                with st.expander("🔍 Workflow details"):
                    st.json(msg["details"])

    if prompt := st.chat_input(
        "Ask a math or leave-balance question…",
        key="supervisor_input",
    ):
        st.session_state.supervisor_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Routing request…"):
                result = st.session_state.supervisor_graph.invoke({"query": prompt})

            worker = result.get("worker", "unknown")
            output = result.get("result", "")
            expression = result.get("expression", "")
            employee_name = result.get("employee_name", "")
            leave_balance = result.get("leave_balance", "")

            if worker == "math":
                st.markdown(f"**Selected worker:** Math Agent")
                st.markdown(f"**Result:** {output}")
                with st.expander("🔍 Workflow details"):
                    st.json(
                        {
                            "Worker": "math",
                            "Expression": expression,
                            "Result": output,
                        }
                    )
                st.session_state.supervisor_messages.append(
                    {
                        "role": "assistant",
                        "content": output,
                        "details": {
                            "Worker": "math",
                            "Expression": expression,
                            "Result": output,
                        },
                    }
                )
            elif worker == "leave":
                st.markdown(f"**Selected worker:** Leave Agent")
                st.markdown(f"**Result:** {output}")
                with st.expander("🔍 Workflow details"):
                    st.json(
                        {
                            "Worker": "leave",
                            "Employee": employee_name,
                            "Leave Balance": leave_balance,
                            "Result": output,
                        }
                    )
                st.session_state.supervisor_messages.append(
                    {
                        "role": "assistant",
                        "content": output,
                        "details": {
                            "Worker": "leave",
                            "Employee": employee_name,
                            "Leave Balance": leave_balance,
                            "Result": output,
                        },
                    }
                )
            else:
                st.markdown(f"**Selected worker:** General Agent")
                st.markdown(f"**Answer:** {output}")
                with st.expander("🔍 Workflow details"):
                    st.json(
                        {
                            "Worker": "general",
                            "Answer": output,
                        }
                    )
                st.session_state.supervisor_messages.append(
                    {
                        "role": "assistant",
                        "content": output,
                        "details": {
                            "Worker": "general",
                            "Answer": output,
                        },
                    }
                )

    with st.sidebar:
        st.header("💡 Supervisor-Worker examples")
        st.markdown(
            """
            - What is the square of the average of 10 and 5?
            - What is the leave balance for Alice?
            - Calculate 25% of 200.
            - What is Bob's leave balance?
            - Define AI
            - Explain machine learning in simple words
            - Who was Albert Einstein?
            """
        )
        if st.button("🗑️ Clear supervisor chat", key="clear_supervisor_chat"):
            st.session_state.supervisor_messages = []
            st.rerun()


# ---------------------------------------------------------------------------
# App entry point
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🏗️ Pattern selector")
    demo_choice = st.radio(
        "Choose a demo",
        ["Tool-Using Agent", "Planner-Executor Agent", "Supervisor-Worker Agent"],
        index=0,
    )

if demo_choice == "Tool-Using Agent":
    render_tool_using_demo()
elif demo_choice == "Planner-Executor Agent":
    render_planner_executor_demo()
else:
    render_supervisor_worker_demo()

st.sidebar.markdown("---")
st.sidebar.caption("Demonstration app for multiple agentic AI workflow patterns.")