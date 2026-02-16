from fastmcp import FastMCP
import httpx

mcp=FastMCP(
    name="Demo MCP",
    instructions="This server used to Understand MCP"
)

@mcp.tool
def add(x:int,y:int) -> int:
    return x+y


@mcp.resource("data://resource")
def get_resource() ->dict:
    return {
        "content":"This Page Helps you to UnderStannd the Concepts of the MCP server"
    }

url = "https://api.openweathermap.org/data/2.5/weather"
WEATHER_KEY="5aec19a2b5426954a665ab8b113e6e5c"
@mcp.tool
async def get_weather(city:str) ->dict:
    "fetching weather"
    params={
        "q":city,
        "appid":WEATHER_KEY,
        "units":"metric"
    }
    headers={
        "Accept":"application/json"
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r=await client.get(url,params=params)
            if r.status_code != 200:
                return {
                    "error": "API failed",
                    "status": r.status_code,
                    "body": r.text
                }

            data = r.json()
            
        
        return {
            "city":data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        return {
            "error":str(e),
            "city":city
        }
        
        
if __name__=="__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
    