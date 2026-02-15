import json
from tool_client import discover_tools, execute_tool
from llm_groq import call_llm

MAX_STEPS = 5


def run_agent(user_query: str):

    print("Discovering MCP tools...")
    tools = discover_tools()
    print("Loaded tools:", [t["name"] for t in tools])

    messages = [
        {"role": "system", "content": "You are a tool-using agent."},
        {"role": "user", "content": user_query}
    ]

    for step in range(MAX_STEPS):

        print(f"\n=== Agent Step {step+1} ===")

        resp = call_llm(messages, tools)

        # ----------------------
        # TOOL CALL CASE
        # ----------------------
        if "tool_calls" in resp:

            call = resp["tool_calls"][0]
            tool_name = call["name"]
            args = call["arguments"]
            call_id = call["id"]

            print("Tool selected:", tool_name)
            print("Arguments:", args)

            tool_resp = execute_tool(tool_name, args)
            print("Server response:", tool_resp)

            if not tool_resp.get("success"):
                messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": json.dumps(tool_resp)
                })
                continue

            messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "content": json.dumps(tool_resp["result"])
            })

            continue

        # ----------------------
        # FINAL ANSWER CASE
        # ----------------------
        return resp["content"]

    # ----------------------
    # LOOP LIMIT HIT
    # ----------------------
    return "Agent stopped — max steps reached"
