from pydantic import BaseModel

class WeatherArgs(BaseModel):
    city:str

tool_validator= {
    "get_weather":WeatherArgs
}