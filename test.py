from fastmcp import Client
import asyncio

async def test():
    async with Client("https://gofastmcp.com/mcp") as client:
        result = await client.call_tool(
            name="SearchFastMcp", 
            arguments={"query": "deploy a FastMCP server"}
        )
    print(result)
asyncio.run(test())