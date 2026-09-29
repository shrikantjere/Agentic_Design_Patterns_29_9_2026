"""
Streamlit frontend for the Tool-Using Agentic AI Workflow.

Provides a chat interface that handles both math expressions
and general questions through a two-agent pipeline with
automatic fallback.
"""

import streamlit as st
from patterns.tool_using.graph import build_graph

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Tool-Using Agent",
    page_icon="🤖",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Title & description
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Initialise session state
# ---------------------------------------------------------------------------
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------------------------
# Display chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "details" in msg:
            with st.expander("🔍 Workflow details"):
                st.json(msg["details"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask a math question or anything else…"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the agent workflow
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            result = st.session_state.graph.invoke({"question": prompt})

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
            st.session_state.messages.append(
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
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "details": {"Query Type": "General", "Answer": answer},
                }
            )

# ---------------------------------------------------------------------------
# Sidebar – example prompts
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("💡 Example prompts")
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
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()