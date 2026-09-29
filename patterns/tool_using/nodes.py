from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState

llm = get_llm()

def classifier(state: AgentState) -> dict:
    """Classify the question as 'math' or 'general'."""
    prompt = f"""
        Classify the following question into exactly one category:
        - "math" if the question is about arithmetic, calculations, numbers, or mathematical expressions
        - "general" for any other type of question (definitions, explanations, facts, opinions, etc.)

        Return ONLY the single word: math or general.

        Question: {state['question']}
        Category:
    """
    category = llm.invoke(prompt).content.strip().lower()
    # Sanity check
    if "math" in category:
        category = "math"
    else:
        category = "general"
    return {"query_type": category}


def reasoning_agent(state: AgentState):
    prompt = f"""
                You are a math reasoning agent.

                Convert the question into a valid Python math expression.
                Return ONLY the expression.

                Examples:
                Question: What is the sum of 5 and 3?
                Expression: 5 + 3

                Question: What is the average of 100 and 200?
                Expression: (100 + 200) / 2

                Question: What is the square of the average of 100 and 200?
                Expression: ((100 + 200) / 2) ** 2

                Question: {state['question']}
                Expression:
                """
    expression = llm.invoke(prompt).content.strip()

    return {"expression": expression}


def tool_executor(state: AgentState):
    result = calculator(state["expression"])
    return {"result": result}


def general_agent(state: AgentState):
    """Answer any general question using the LLM."""
    prompt = f"""
        You are a helpful, knowledgeable assistant.
        Answer the following question clearly and concisely.

        Question: {state['question']}
        Answer:
    """
    answer = llm.invoke(prompt).content.strip()
    return {"answer": answer}