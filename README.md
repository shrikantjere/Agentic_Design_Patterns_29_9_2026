# 🤖 Tool-Using Agentic AI Workflow

A **LangGraph**-powered agentic workflow that intelligently routes user queries to the right agent — either a **math reasoning agent** (for arithmetic / calculation questions) or a **general-purpose LLM agent** (for definitions, explanations, and any other question).

## ✨ Features

- **Smart query classification** — automatically detects whether a question is math-related or general.
- **Math expression engine** — converts natural-language math questions into Python expressions and evaluates them.
- **General fallback** — answers any non-math question using GPT-4o-mini.
- **Streamlit chat UI** — clean, interactive frontend with chat history and workflow details.
- **Modular architecture** — easy to extend with new tools and agents.

## 🧠 Architecture

```
                    ┌──────────────┐
                    │  Classifier  │
                    │  (LLM-based) │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
       ┌──────▼──────┐          ┌──────▼───────┐
       │  Math path  │          │  General path │
       │             │          │              │
       │ Reasoning   │          │  General      │
       │ Agent       │          │  Agent (LLM)  │
       │ (LLM → expr)│          │              │
       │             │          └──────┬───────┘
       │ Math Agent  │                 │
       │ (eval)      │                 │
       └──────┬──────┘                 │
              │                        │
              └──────────┬─────────────┘
                         │
                   ┌─────▼─────┐
                   │    END    │
                   └───────────┘
```

### Components

| Component | File | Role |
|-----------|------|------|
| **State** | `patterns/tool_using/state.py` | TypedDict defining the workflow state |
| **Nodes** | `patterns/tool_using/nodes.py` | Agent functions: classifier, reasoning_agent, tool_executor, general_agent |
| **Graph** | `patterns/tool_using/graph.py` | LangGraph state graph with conditional routing |
| **Runner** | `patterns/tool_using/run.py` | CLI entry point for testing |
| **Calculator** | `tools/calculator.py` | Safe `eval()` wrapper for math expressions |
| **LLM Config** | `config/llm.py` | OpenAI / LangChain LLM initialisation |
| **Frontend** | `app.py` | Streamlit chat interface |

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/shrikantjere/Agentic_Design_Patterns_29_9_2026.git
cd Agentic_Design_Patterns_29_9_2026

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate    # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your OpenAI API key
cp .env.example .env       # then edit .env with your key
```

### Run the CLI test

```bash
python -m patterns.tool_using.run
```

### Run the Streamlit frontend

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

## 💬 Example Queries

| Type | Question |
|------|----------|
| Math | `What is 15 + 27?` |
| Math | `What is the average of 100 and 200?` |
| Math | `Compute (12 + 8) * 5` |
| Math | `What is the square of 9?` |
| General | `Define AI` |
| General | `What is machine learning?` |
| General | `Explain the theory of relativity` |
| General | `Who wrote Romeo and Juliet?` |

## 🛠️ Project Structure

```
.
├── app.py                          # Streamlit frontend
├── config/
│   └── llm.py                      # LLM configuration (OpenAI)
├── patterns/
│   └── tool_using/
│       ├── __init__.py
│       ├── graph.py                # LangGraph state graph
│       ├── nodes.py                # Agent node functions
│       ├── run.py                  # CLI entry point
│       └── state.py                # Workflow state definition
├── tools/
│   ├── __init__.py
│   └── calculator.py               # Math expression evaluator
├── requirements.txt
├── .env.example
└── README.md
```

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.