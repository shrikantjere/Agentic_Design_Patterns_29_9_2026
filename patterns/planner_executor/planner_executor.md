# 📋 Planner-Executor Pattern

## 🧩 What is this pattern?

The **Planner-Executor** pattern is an agentic AI workflow where the system first **plans** how to solve a task, and then **executes** each step of that plan one by one.

Think of it like a **manager + worker** setup:

| Role | Agent | What it does |
|------|-------|-------------|
| 🧠 **Manager** | `planner` | Reads the task and breaks it into small, clear steps |
| ⚡ **Worker** | `executor` | Takes each step and actually does it |

---

## 🏗️ How the code is organised

```
patterns/planner_executor/
├── state.py      # Defines what data flows through the workflow
├── nodes.py      # Contains the planner and executor agent functions
├── graph.py      # Wires the agents together into a flow
└── run.py        # Entry point to test the workflow
```

---

## 📦 1. State — `state.py`

The **state** is like a shared whiteboard that both agents read from and write to.

```python
from typing import TypedDict, List

class PlanState(TypedDict):
    task: str        # The original user task (e.g., "Explain Python basics")
    plan: List[str]  # The list of steps the planner creates
    output: str      # The final answer after all steps are executed
```

**Flow of data:**
1. You provide a `task` → the planner reads it
2. The planner writes a `plan` (list of steps)
3. The executor reads the `plan`, runs each step, and writes the final `output`

---

## 🧠 2. Planner Agent — `nodes.py` (part 1)

The **planner** is an LLM-based agent that takes your task and breaks it into steps.

```python
def planner(state: PlanState):
    prompt = f"""
        You are a planning agent.
        Break the task into AT MOST 3 steps.
        Each step MUST start with a dash (-).

        Task: {state['task']}
        Plan:
    """
    response = llm.invoke(prompt).content.strip()
    plan = response.split("\n")   # Convert to a list of steps
    return {"plan": plan}
```

**What happens:**
- The LLM reads your task (e.g., *"Explain Python basics"*)
- It returns a plan like:
  ```
  - Explain what Python is
  - Give 2 simple Python examples
  - Create 2 quiz questions
  ```
- These lines are split into a Python list: `["- Explain what Python is", "- Give 2 simple Python examples", ...]`
- The list is saved into `state["plan"]`

---

## ⚡ 3. Executor Agent — `nodes.py` (part 2)

The **executor** loops through each step in the plan and executes it one by one.

```python
def executor(state: PlanState):
    results = []
    for step in state["plan"]:
        step = step.strip()
        if not step or not step.startswith("-"):
            continue          # Skip empty or invalid steps
        prompt = f"Execute the following step clearly and concisely.\nStep:\n{step}"
        response = llm.invoke(prompt).content
        results.append(response)
    return {"output": "\n\n".join(results)}
```

**What happens:**
- It takes the first step: `"- Explain what Python is"`
- It asks the LLM: *"Execute this step clearly and concisely"*
- The LLM returns an explanation of what Python is
- It moves to the next step and repeats
- All answers are joined together into the final `output`

---

## 🔗 4. Graph — `graph.py`

The **graph** defines the order in which agents run. It uses **LangGraph** (`StateGraph`).

```python
def build_graph():
    graph = StateGraph(PlanState)

    graph.add_node("planner", planner)     # Add the planner agent
    graph.add_node("executor", executor)   # Add the executor agent

    graph.set_entry_point("planner")       # Start with the planner
    graph.add_edge("planner", "executor")  # After planner → run executor
    graph.add_edge("executor", END)        # After executor → finish

    return graph.compile()
```

**Visual flow:**

```
   ┌──────────┐       ┌──────────┐       ┌─────┐
   │ Planner  │──────▶│ Executor │──────▶│ END │
   │ (plan)   │       │ (do it)  │       │     │
   └──────────┘       └──────────┘       └─────┘
```

---

## 🚀 5. Running it — `run.py`

```python
from patterns.planner_executor.graph import build_graph

def run_task(task: str):
    app = build_graph()
    return app.invoke({"task": task})

result = run_task("Create a simple 3-step plan for launching an AI chatbot product.")
print(result["output"])   # The final answer
```

---

## 🧪 Example Walkthrough

Let's trace what happens when you ask:

> *"Explain Python basics"*

### Step 1 — Planner runs
```
[Planner] Creating execution plan...
[Planner] Generated plan:
- Explain what Python is
- Give 2 simple Python examples
- Create 2 quiz questions
```

### Step 2 — Executor runs each step
```
[Executor] Running step: - Explain what Python is
[Executor] Running step: - Give 2 simple Python examples
[Executor] Running step: - Create 2 quiz questions
```

### Step 3 — Final output is assembled
The LLM's answer to each step is combined into one final response.

---

## 💡 When to use this pattern

| ✅ Use it when... | ❌ Don't use it when... |
|------------------|------------------------|
| The task has multiple clear sub-steps | The task is a single simple question |
| You want the LLM to "show its working" | You need real-time tool calling |
| You need structured, step-by-step output | The steps depend on each other's results |
| The plan is predictable from the task | The task needs dynamic re-planning |

---

## 🔄 How it's different from the Tool-Using pattern

| Feature | Planner-Executor | Tool-Using |
|---------|-----------------|------------|
| **Flow** | Plan first, then execute all steps | Classify first, then route to one agent |
| **Steps** | Multiple steps executed sequentially | Single agent handles the query |
| **Best for** | Complex multi-step tasks | Simple questions or calculations |
| **Fallback** | No — always plans & executes | Yes — classifier routes to general agent |

---

## 🧠 Key Takeaways for Beginners

1. **Planner = "what to do"** — breaks the big task into small pieces
2. **Executor = "do it"** — works through each piece one at a time
3. **State = shared memory** — both agents read/write to the same `PlanState`
4. **Graph = the wiring** — defines which agent runs when
5. The LLM does the actual thinking — the code just orchestrates the flow