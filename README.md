# 🌉 MCP Bridge Architecture — FastAPI + MCP Server

A production-style bridge architecture that connects a FastAPI web layer with an MCP tool server using a persistent async connection. This design allows you to expose AI tools (like weather lookup) across your network efficiently and safely.

---

## ✅ What This Project Demonstrates

- MCP client/server tool communication
- FastAPI lifespan-based persistent connections
- Async context management with AsyncExitStack
- Handshake-aware MCP usage
- Low-latency tool calling through a bridge layer
- Clean separation between API layer and tool worker

---

## 🧠 Architecture Overview

This project builds a Bridge.

- One side: MCP Server — the worker that knows how to fetch weather data
- Other side: FastAPI Server — the manager that exposes a friendly API
- Middle: Bridge Layer (MCPManager) — maintains a persistent MCP connection

Instead of calling the weather API directly, your app asks the Bridge, the Bridge asks the MCP Server, and the results flow back.

Client App → FastAPI Bridge → Persistent MCP Client → MCP Server Tool → Weather API

This architecture allows you to share AI tools across multiple apps and services.

---

## ⚠️ Error Log — Connection Puzzles & Fixes

The most important learning came from debugging MCP connection issues.

### 🧩 Error 1 — No Handshake Error

Error:

RuntimeError: Client is not connected. Use the 'async with client:' context manager first.

Why it happened:

MCP is stateful. It requires a handshake before tool calls are allowed.

Fix:

Use:

async with Client(...)

This ensures:
- Connection opens
- Handshake completes
- Tools become callable
- Cleanup happens safely

---

### 🧩 Error 2 — Handshake Latency Problem

Problem:

Each /weather request created a new MCP connection + handshake.

Why it matters:
- Each handshake costs ~100–300ms
- High traffic → handshake storm
- Server slowdown

Fix:

Move connection into FastAPI lifespan.

Result:
- Connect once at startup
- Reuse connection for all requests
- Close once at shutdown

---

### 🧩 Error 3 — 404 Not Found

Error:

httpx.HTTPStatusError: 404 Not Found for /sse

Cause:

Client path didn’t match server path.
Client expected /sse
Server exposed /mcp

Fix:

Align client URL exactly with MCP server route.

---

## ⚙️ Advanced Concepts Used

### Async Programming (async/await)

Async lets the server handle other users while waiting for tool/API responses.

Like a waiter serving multiple tables instead of waiting at the kitchen.

await tool_call()

---

### AsyncExitStack — Context Backpack

A reusable container for async context managers.

Normal:
async with client → closes immediately after block

AsyncExitStack:
- Enter once
- Keep open globally
- Close later manually
- Share connection across routes

---

### FastAPI Lifespan Events

Controls startup and shutdown behavior.

Used here to manage MCP connection lifecycle.

Startup → Connect to MCP  
Runtime → Reuse connection  
Shutdown → Close connection

---

## 📁 Final Code Structure

project/
├── client.py
├── mcp_manager.py
└── README.md

---

## 🧩 mcp_manager.py — Connection Hub

```python
from contextlib import AsyncExitStack
from fastmcp import Client

class MCPManager:
    def __init__(self, url: str):
        self.url = url
        self.client = Client(self.url)
        self._stack = AsyncExitStack()

    async def connect(self):
        await self._stack.enter_async_context(self.client)
        print(f"✅ Persistent MCP Connection Active: {self.url}")

    async def disconnect(self):
        await self._stack.aclose()
        print("🔌 MCP Connection Closed.")

mcp_hub = MCPManager("http://127.0.0.1:8000/mcp")
```

---

## 🌐 client.py — FastAPI Bridge

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from mcp_manager import mcp_hub

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mcp_hub.connect()
    yield
    await mcp_hub.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/weather")
async def weather_route(city: str):
    return await mcp_hub.client.call_tool(
        "get_weather",
        {"city": city}
    )
```

---

## 🚀 Quick Start (Under 2 Minutes)

1. Start MCP Server
python mcp_server.py

2. Start FastAPI Bridge
uvicorn client:app --reload

3. Call Weather Endpoint
curl -X POST "http://127.0.0.1:8001/weather?city=London"

---

## 📊 Beginner Summary Table

Concept | Simple Meaning | Use Case
Stdio | Local cable | Desktop tool apps
HTTP/SSE | Remote link | Web/cloud tools
Context Manager | Handshake + cleanup | Required for MCP
Async | Non-blocking work | Tool/API calls
Lifespan | Startup/shutdown hooks | Persistent connections

---

## 🎯 Why This Pattern Is Powerful

- Eliminates repeated MCP handshakes
- Reduces latency
- Supports high concurrency
- Clean architecture separation
- Tool servers become reusable infrastructure
- Works well for AI agents & MCP ecosystems

---

## 📌 License

MIT — use freely for learning and building AI tool infrastructure.
