# 🤖 MCP Tool-Calling Agent

A Python-based AI agent that implements the **Model Context Protocol (MCP)**. This project demonstrates how an LLM (Groq) can dynamically discover local tools and execute them to solve complex user queries.

---

## 🌟 Project Highlights

- **ReAct Framework:** Implements a "Reason-Act" loop where the AI thinks, acts via tools, and observes results.
- **Dynamic Discovery:** Automatically fetches available tools from a local server.
- **State Management:** Maintains conversation history and tracks unique `tool_call_id` for accurate responses.
- **Production Ready:** Includes error handling for server communication and a loop-limit (MAX_STEPS) to prevent infinite AI loops.

---

## 🏗 Architecture

The project is divided into three main layers:

1.  **The Orchestrator (`main.py`):** The "brain" that manages the loop.
2.  **The Tool Client (`tool_client.py`):** The "hands" that talk to your local API.
3.  **The LLM Integration (`llm_groq.py` / `llm_stub.py`):** The "intelligence" powered by Groq.



---

## 🛠 File Breakdown

| File | Purpose |
| :--- | :--- |
| `main.py` | Contains the `run_agent` loop and state management logic. |
| `tool_client.py` | Uses `requests` to call `/tools` and `/execute` endpoints. |
| `llm_groq.py` | Connects to the Groq API for real-time tool selection. |
| `llm_stub.py` | A local mock function for testing logic without API calls. |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed and the `requests` library:
```bash
pip install requests
