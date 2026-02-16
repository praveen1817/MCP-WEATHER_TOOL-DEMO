import asyncio
from fastmcp import Client
from pydantic import BaseModel
from fastapi import FastAPI


app=FastAPI()

mcpClient=Client("http://127.0.0.1:8000/mcp")

class weatherArgs(BaseModel):
    city:str
    
@app.post('/weather')
async def client(req:weatherArgs):
    async with mcpClient as client:
        print("service Started")        
        await client.ping()

        
        result= await client.call_tool(
            "get_weather",
            {"city":req.city}
        )
        print(result)
        return {
            "source":"mcp",
            "data":result
        }
            
            
            