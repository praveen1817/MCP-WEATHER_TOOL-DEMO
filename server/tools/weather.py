def get_weather(city:str):
    fake_db={
        "chennai":30,
        "coimbatore":40,
        "salem":23
    }
    lower_city=city.lower()

    if lower_city not in fake_db:
        raise ValueError("City not found")
    
    return {
        "city": city,
        "temperature": fake_db[lower_city],
        "unit": "C"
    }