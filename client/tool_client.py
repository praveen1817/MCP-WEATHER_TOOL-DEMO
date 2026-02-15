import requests


MCP_BASE="http://127.0.0.1:8000"

def discover_tools():
    r= requests.get(f"{MCP_BASE}/tools",timeout=5)
    r.raise_for_status()
    data=r.json()
    
    if "tools" not in data:
        raise RuntimeError("Expected 'tools' in response data")
    return data["tools"]

def execute_tool(tool_name:str,arguments:dict):

    payLoad={
        "tool_name":tool_name,
        "arguments":arguments
    }

    r=requests.post(f"{MCP_BASE}/execute",json=payLoad,timeout=10)
    
    r.raise_for_status()
    return r.json()
