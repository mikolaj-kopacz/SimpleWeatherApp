import json
import tkinter as tk
from get_weather import Weather

from geopy.geocoders.base import Geocoder
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim
from geopy import geocoders

class GUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("800x600")
        self.root.config(background="#00b4d8")
        self.root.title("Simple Weather App")

        self.last_lat = 50.037379
        self.last_lon = 22.005030
        self.weather = Weather()
        self.ui_design()
        self.root.mainloop()



    def ui_design(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.config(background="#00b4d8", padx=25, pady=25)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_frame.grid_columnconfigure(0, weight=0, minsize=100)
        self.main_frame.grid_columnconfigure(1, weight=1, minsize=150)
        self.main_frame.grid_columnconfigure(2, weight=0, minsize=100)
        self.main_frame.grid_columnconfigure(3, weight=1, minsize=150)

        self.label_enter_city = tk.Label(self.main_frame, text="Enter your city: ", bg="#00b4d8")
        self.label_enter_city.grid(row=0, column=0, sticky="w")

        self.entry_city = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7",fg="black",
                                   highlightbackground="#0096c7")
        self.entry_city.grid(row=0, column=1, sticky="ew", padx=(0, 20))

        self.label_enter_zip_code = tk.Label(self.main_frame, text="Enter Zip Code: ", bg="#00b4d8")
        self.label_enter_zip_code.grid(row=0, column=2, sticky="w")

        self.entry_zip_code = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7",
                                       highlightbackground="#0096c7",fg="black")
        self.entry_zip_code.grid(row=0, column=3, sticky="ew")

        self.label_pick_a_city = tk.Label(self.main_frame, text="Or choose from map", bg="#00b4d8")
        self.label_pick_a_city.grid(row=2, column=0, sticky="w", pady=5)

        self.button_pick_a_city = tk.Button(self.main_frame, text="Pick A City", command=self.open_map,
                                            highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_pick_a_city.grid(row=2, column=1, sticky="w", pady=5)

        self.label_picked_city = tk.Label(self.main_frame, text="", bg="#00b4d8", fg="black",pady=(50))
        self.label_picked_city.grid(row=3, column=0, columnspan=4, sticky="w")

        self.button_search = tk.Button(self.main_frame, text="Search",command=self.search_for_coords,highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_search.grid(row=0, column=4, columnspan=4, )

        self.image_sunny = tk.PhotoImage(file="images/sunny.png")
        self.image_cloudy = tk.PhotoImage(file="images/cloudy.png")
        self.image_rainy = tk.PhotoImage(file="images/rainy.png")
        self.image_snowy = tk.PhotoImage(file="images/snowy.png")


    def open_map(self):
        map_window = tk.Toplevel(self.root)
        map_window.geometry("600x600")
        map_window.title("Choose your location")

        map_window.grid_rowconfigure(0, weight=1)
        map_window.grid_rowconfigure(1, weight=0)
        map_window.grid_columnconfigure(0, weight=1)

        map_view = TkinterMapView(map_window)
        map_view.set_position(self.last_lat, self.last_lon)
        map_view.set_zoom(10.0)
        map_view.grid(row=0, column=0, sticky="nsew")

        def click(coords):
            lat, lon = coords
            self.last_lat = lat
            self.last_lon = lon
            geolocator = Nominatim(user_agent="weather-app")
            location = geolocator.reverse((lat, lon), language="en")

            if location and location.address:
                address = location.raw.get("address", {})
                city = address.get("city") or address.get("town") or address.get("village") or ""
                zipcode = address.get("postcode", "")

                self.label_picked_city.config(text=f"{city} {zipcode}")
                map_view.set_position(lat, lon)
            else:
                self.label_picked_city.config(text=f"{lat:.5f}, {lon:.5f}")

        map_view.add_left_click_map_command(click)

        def close_map():
            map_window.destroy()
            weather_data = self.weather.get_weather(self.last_lat, self.last_lon)


        button_close = tk.Button(map_window, text="Close and Save", command=close_map)
        button_close.grid(row=1, column=0, sticky="e", pady=(4, 4), padx=10)

    def search_for_coords(self):
        city_text = self.entry_city.get().strip()
        zip_text = self.entry_zip_code.get().strip()

        if not city_text and not zip_text:
            self.label_picked_city.config(text="Enter a city or zip code")
            return

        self.label_picked_city.config(text=f"Weather for: {city_text.capitalize()} {zip_text}")
        query = f"{zip_text} {city_text}".strip()

        try:
            geolocator = Nominatim(user_agent="weather-app")
            location = geolocator.geocode(query)
            if location:
                self.last_lat = location.latitude
                self.last_lon = location.longitude
                address = location.raw.get("address", {})
                self.city = address.get("city") or address.get("town") or address.get("village") or ""
                self.zipcode = address.get("postcode", "")

            else:
                self.label_picked_city.config(text="Location not found")
        except Exception as e:
            self.label_picked_city.config(text="Error connecting to geocoder")

        self.show_weather()

    def show_weather(self):
        weather_data = self.weather.get_weather(self.last_lat, self.last_lon)
        print(weather_data)

        # Prognoza 1 (indeks 0)
        temp_current = int(weather_data["list"][0]["main"]["temp"])
        weather_current = weather_data["list"][0]["weather"][0]["main"]
        weather_current_description = weather_data["list"][0]["weather"][0]["description"]
        weather_current_time = weather_data["list"][0]["dt_txt"].split()[1][:5]

        current_time_label = tk.Label(self.main_frame, text=f"{weather_current_time}", bg="#00b4d8", fg="black")
        current_time_label.grid(row=5, column=0, sticky="nsew")
        current_label = tk.Label(self.main_frame, text=f"Temperature: {temp_current}C", bg="#00b4d8", fg="black")
        current_label.grid(row=6, column=0)

        if weather_current == "Rain":
            image = self.image_rainy
        elif weather_current == "Clouds":
            image = self.image_cloudy
        elif weather_current == "Snow":
            image = self.image_snowy
        elif weather_current == "Clear":
            image = self.image_sunny
        else:
            image = self.image_sunny

        self.current_weather_label = tk.Label(self.main_frame, image=image, bg="#00b4d8", pady=40)
        self.current_weather_label.grid(row=4, column=0)

        # Prognoza 2 (indeks 1)
        temp_current_1 = int(weather_data["list"][1]["main"]["temp"])
        weather_current_1 = weather_data["list"][1]["weather"][0]["main"]
        weather_current_description_1 = weather_data["list"][1]["weather"][0]["description"]
        weather_current_time_1 = weather_data["list"][1]["dt_txt"].split()[1][:5]

        current_time_label_1 = tk.Label(self.main_frame, text=f"{weather_current_time_1}", bg="#00b4d8", fg="black")
        current_time_label_1.grid(row=5, column=1, sticky="nsew")
        current_label_1 = tk.Label(self.main_frame, text=f"Temperature: {temp_current_1}C", bg="#00b4d8", fg="black")
        current_label_1.grid(row=6, column=1)

        if weather_current_1 == "Rain":
            image = self.image_rainy
        elif weather_current_1 == "Clouds":
            image = self.image_cloudy
        elif weather_current_1 == "Snow":
            image = self.image_snowy
        elif weather_current_1 == "Clear":
            image = self.image_sunny
        else:
            image = self.image_sunny

        self.current_weather_label_1 = tk.Label(self.main_frame, image=image, bg="#00b4d8", pady=20)
        self.current_weather_label_1.grid(row=4, column=1)

        # Prognoza 3 (indeks 2)
        temp_current_2 = int(weather_data["list"][2]["main"]["temp"])
        weather_current_2 = weather_data["list"][2]["weather"][0]["main"]
        weather_current_description_2 = weather_data["list"][2]["weather"][0]["description"]
        weather_current_time_2 = weather_data["list"][2]["dt_txt"].split()[1][:5]

        current_time_label_2 = tk.Label(self.main_frame, text=f"{weather_current_time_2}", bg="#00b4d8", fg="black")
        current_time_label_2.grid(row=5, column=2, sticky="nsew")
        current_label_2 = tk.Label(self.main_frame, text=f"Temperature: {temp_current_2}C", bg="#00b4d8", fg="black")
        current_label_2.grid(row=6, column=2)

        if weather_current_2 == "Rain":
            image = self.image_rainy
        elif weather_current_2 == "Clouds":
            image = self.image_cloudy
        elif weather_current_2 == "Snow":
            image = self.image_snowy
        elif weather_current_2 == "Clear":
            image = self.image_sunny
        else:
            image = self.image_sunny

        self.current_weather_label_2 = tk.Label(self.main_frame, image=image, bg="#00b4d8", pady=20)
        self.current_weather_label_2.grid(row=4, column=2)

        # Prognoza 4 (indeks 3)
        temp_current_3 = int(weather_data["list"][3]["main"]["temp"])
        weather_current_3 = weather_data["list"][3]["weather"][0]["main"]
        weather_current_description_3 = weather_data["list"][3]["weather"][0]["description"]
        weather_current_time_3 = weather_data["list"][3]["dt_txt"].split()[1][:5]

        current_time_label_3 = tk.Label(self.main_frame, text=f"{weather_current_time_3}", bg="#00b4d8", fg="black")
        current_time_label_3.grid(row=5, column=3, sticky="nsew")
        current_label_3 = tk.Label(self.main_frame, text=f"Temperature: {temp_current_3}C", bg="#00b4d8", fg="black")
        current_label_3.grid(row=6, column=3)

        if weather_current_3 == "Rain":
            image = self.image_rainy
        elif weather_current_3 == "Clouds":
            image = self.image_cloudy
        elif weather_current_3 == "Snow":
            image = self.image_snowy
        elif weather_current_3 == "Clear":
            image = self.image_sunny
        else:
            image = self.image_sunny

        self.current_weather_label_3 = tk.Label(self.main_frame, image=image, bg="#00b4d8", pady=20)
        self.current_weather_label_3.grid(row=4, column=3)

        # Prognoza 5 (indeks 4)
        temp_current_4 = int(weather_data["list"][4]["main"]["temp"])
        weather_current_4 = weather_data["list"][4]["weather"][0]["main"]
        weather_current_description_4 = weather_data["list"][4]["weather"][0]["description"]
        weather_current_time_4 = weather_data["list"][4]["dt_txt"].split()[1][:5]

        current_time_label_4 = tk.Label(self.main_frame, text=f"{weather_current_time_4}", bg="#00b4d8", fg="black")
        current_time_label_4.grid(row=5, column=4, sticky="nsew")
        current_label_4 = tk.Label(self.main_frame, text=f"Temperature: {temp_current_4}C", bg="#00b4d8", fg="black")
        current_label_4.grid(row=6, column=4)

        if weather_current_4 == "Rain":
            image = self.image_rainy
        elif weather_current_4 == "Clouds":
            image = self.image_cloudy
        elif weather_current_4 == "Snow":
            image = self.image_snowy
        elif weather_current_4 == "Clear":
            image = self.image_sunny
        else:
            image = self.image_sunny

        self.current_weather_label_4 = tk.Label(self.main_frame, image=image, bg="#00b4d8", pady=20)
        self.current_weather_label_4.grid(row=4, column=4)

