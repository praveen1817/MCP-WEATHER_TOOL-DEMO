from tools.weather import get_weather

weather_schema = {
    "name": "get_weather",
    "description": "Get temperature for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"}
        },
        "required": ["city"]
    }
}

TOOL_REGISTRY = {
    "get_weather": {
        "func": get_weather,
        "schema": weather_schema
    }
}
