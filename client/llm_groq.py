import json
from groq import Groq

client = Groq(api_key="Your API Key")

MODEL = "llama-3.3-70b-versatile"


def adapt_tools_for_groq(mcp_tools):
    out = []
    for t in mcp_tools:
        out.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t["parameters"]
            }
        })
    return out


def call_llm(messages, tools):

    groq_tools = adapt_tools_for_groq(tools)

    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=messages,
        tools=groq_tools,
        tool_choice="auto"
    )

    msg = resp.choices[0].message

    if msg.tool_calls:
        calls = []
        for tc in msg.tool_calls:
            calls.append({
            "id": tc.id,
            "name": tc.function.name,
            "arguments": json.loads(tc.function.arguments)
        })
            
        return {"tool_calls": calls}


    return {"content": msg.content}
