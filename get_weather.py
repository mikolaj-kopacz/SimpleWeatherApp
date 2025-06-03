import requests

class Weather:
    def __init__(self):
        self.api_key = "6351d5b8402729dd6d182fc6d4dc4a06"
        self.lang  = "en"
        self.units = "metric"

    def get_weather(self,lat,lon):
        response = requests.get(f"https://pro.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&lang={self.lang}&units={self.units}")
        return response.json()



