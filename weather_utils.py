import requests
import urllib.request
import os
from geopy.geocoders import Nominatim



class Weather:
    def __init__(self):
        self.api_key = "YOUR_API_KEY_HERE"
        self.lang = "en"
        self.units = "metric"
        self.geolocator = Nominatim(user_agent="weather-app")

    def get_weather(self, lat, lon):
        response = requests.get(
            f"https://pro.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&lang={self.lang}&units={self.units}"
        )
        return response.json()

    def get_location_from_coords(self, lat, lon):
        try:
            location = self.geolocator.reverse((lat, lon), language="en")
            if location and location.address:
                address = location.raw.get("address", {})
                city = address.get("city") or address.get("town") or address.get("village") or ""
                zipcode = address.get("postcode", "")
                return {
                    "city": city,
                    "zipcode": zipcode,
                    "display_text": f"Weather for: {city} {zipcode}" if city else f"{lat:.5f}, {lon:.5f}",
                    "success": True
                }
            else:
                return {
                    "city": "",
                    "zipcode": "",
                    "display_text": f"{lat:.5f}, {lon:.5f}",
                    "success": False
                }
        except Exception as e:
            return {
                "city": "",
                "zipcode": "",
                "display_text": "Error retrieving location",
                "success": False,
                "error": str(e)
            }

    def get_coords_from_query(self, city_text, zip_text):
        if not city_text and not zip_text:
            return {"success": False, "error": "Enter a city or zip code"}

        query = f"{zip_text} {city_text}".strip()

        try:
            location = self.geolocator.geocode(query)
            if location:
                address = location.raw.get("address", {})
                return {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "city": address.get("city") or address.get("town") or address.get("village") or "",
                    "zipcode": address.get("postcode", ""),
                    "display_text": f"Weather for: {city_text.capitalize()} {zip_text}",
                    "success": True
                }
            else:
                return {"success": False, "error": "Location not found"}
        except Exception as e:
            return {"success": False, "error": "Error connecting to geocoder"}

    def download_weather_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        os.makedirs("icons", exist_ok=True)
        icon_path = os.path.join("icons", f"{icon_code}.png")

        if not os.path.exists(icon_path):
            try:
                urllib.request.urlretrieve(icon_url, icon_path)
            except Exception as e:
                print(f"Error downloading icon: {e}")
                return None

        return icon_path

    def get_weather_data_for_display(self, lat, lon, start_index=0, count=5):
        try:
            weather_data = self.get_weather(lat, lon)
            processed_data = []

            if "list" not in weather_data:
                return {"success": False, "error": "Invalid weather data", "data": []}

            for i in range(start_index, min(start_index + count, len(weather_data["list"]))):
                item = weather_data["list"][i]
                processed_item = {
                    "temperature": int(item["main"]["temp"]),
                    "description": item["weather"][0]["description"].capitalize(),
                    "time": item["dt_txt"].split()[1][:5],
                    "icon_code": item["weather"][0]["icon"],
                    "icon_path": self.download_weather_icon(item["weather"][0]["icon"])
                }
                processed_data.append(processed_item)

            return {"success": True, "data": processed_data}
        except Exception as e:
            return {"success": False, "error": str(e), "data": []}