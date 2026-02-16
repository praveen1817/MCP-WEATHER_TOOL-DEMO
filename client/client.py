from contextlib import asynccontextmanager
from fastmcp import Client
from pydantic import BaseModel
from fastapi import FastAPI
from mcp_manager import mcp_hub


@asynccontextmanager
async def lifespan(app:FastAPI):
    await mcp_hub.connect()
    yield
    
    await mcp_hub.disconnect()
    

app=FastAPI(lifespan=lifespan)

class weatherArgs(BaseModel):
    city:str
    
@app.post('/weather')
async def client(req:weatherArgs):
    print("service Started")        
    result= await mcp_hub.client.call_tool(
        "get_weather",
        {"city":req.city}
    )
    print(result)
    return {
        "source":"mcp",
        "data":result
    }
            
            
            