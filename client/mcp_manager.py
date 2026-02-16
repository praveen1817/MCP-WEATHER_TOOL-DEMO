from fastmcp import Client
from contextlib import AsyncExitStack

class MCPContextManager:
    def __init__(self,url:str):
        self.url=url
        self.client=Client(self.url)
        self._stack=AsyncExitStack()
    async def connect(self):
        await self._stack.enter_async_context(self.client)
        print(f"Connect to Client at {self.url}")
    async def disconnect(self):
        await self._stack.aclose()
        print("🔌 Disconnected from MCP Server")

mcp_hub = MCPContextManager("http://127.0.0.1:8000/mcp")
        
        