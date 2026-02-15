from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from registry import TOOL_REGISTRY
from validator import tool_validator
app = FastAPI()

@app.get("/tools")

def list_tools():
    return {
        "tools": [
            tool["schema"]
            for tool in TOOL_REGISTRY.values()
        ]
    }

class ToolExecutionRequest(BaseModel):
    tool_name:str
    arguments:dict



@app.post("/execute")
def execute_tool(req: ToolExecutionRequest):
    if req.tool_name not in TOOL_REGISTRY:
        raise HTTPException(404, "Tool not found")

    tool_entry = TOOL_REGISTRY[req.tool_name]

    # 2. Update this line:
    validator = tool_validator[req.tool_name]

    try:
        # Note: validated.dict() is deprecated in Pydantic v2. 
        # Use validated.model_dump() if you're on the newer version!
        validated = validator(**req.arguments)
        result = tool_entry["func"](**validated.model_dump()) 

        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}