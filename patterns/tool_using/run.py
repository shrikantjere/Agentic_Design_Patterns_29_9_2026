from .graph import build_graph

app = build_graph()


def ask(question: str) -> dict:
    """Run the agent workflow and return the final state."""
    return app.invoke({"question": question})


if __name__ == "__main__":
    # Test math question
    r1 = ask("What is the sum of 5 and 3?")
    print("Math question result:")
    print(f"  Question: {r1['question']}")
    print(f"  Expression: {r1['expression']}")
    print(f"  Result: {r1['result']}")
    print()

    # Test general question
    r2 = ask("Define AI")
    print("General question result:")
    print(f"  Question: {r2['question']}")
    print(f"  Answer: {r2['answer']}")
