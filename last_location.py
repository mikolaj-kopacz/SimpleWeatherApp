import json
import os

class LastLocation:
    def __init__(self, filename="last_location.json"):
        self.filename = filename

    def save(self, city, zipcode, lat, lon):
        data = {
            "city": city,
            "zipcode": zipcode,
            "lat": lat,
            "lon": lon
        }
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving last location: {e}")

    def load(self):
        if not os.path.exists(self.filename):
            return None
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            print(f"Error loading last location: {e}")
            return None