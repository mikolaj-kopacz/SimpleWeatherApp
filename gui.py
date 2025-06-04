import tkinter as tk
from get_weather import Weather
import urllib.request
import os

from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

class GUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("800x600")
        self.root.config(background="#00b4d8")
        self.root.title("Simple Weather App")
        self.icon = tk.PhotoImage(file="icons/icons8-weather-forecast-100.png")
        self.root.iconphoto(True, self.icon)
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
        self.entry_city.focus_set()

    def open_map(self):
        map_window = tk.Toplevel(self.root)
        map_window.geometry("600x600")
        map_window.title("Choose your location")

        map_window.grid_rowconfigure(0, weight=1)
        map_window.grid_rowconfigure(1, weight=0)
        map_window.grid_columnconfigure(0, weight=1)

        map_view = TkinterMapView(map_window)
        map_view.set_position(self.last_lat, self.last_lon)
        map_view.set_zoom(10)
        map_view.grid(row=0, column=0, sticky="nsew")
        self.entry_city.delete(0, tk.END)
        self.entry_zip_code.delete(0, tk.END)
        if hasattr(self, "previous_button") and self.previous_button:
            self.previous_button.destroy()

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
            self.show_weather()

        button_close = tk.Button(map_window, text="Close and Save", command=close_map)
        button_close.grid(row=1, column=0, sticky="e", pady=(4, 4), padx=10)

        self.button_next_page = tk.Button(self.main_frame, text="Next",command=self.next_page, highlightbackground="#00b4d8",
                                          activebackground="#0096c7")
        self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    def search_for_coords(self):
        city_text = self.entry_city.get().strip()
        zip_text = self.entry_zip_code.get().strip()
        self.entry_city.delete(0, "end")
        self.entry_zip_code.delete(0, "end")
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
        if hasattr(self, "previous_button") and self.previous_button:
            self.previous_button.destroy()
        self.button_next_page = tk.Button(self.main_frame, text="Next",command=self.next_page,highlightbackground="#00b4d8",
                                          activebackground="#0096c7")
        self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    def show_weather(self):
        weather_data = self.weather.get_weather(self.last_lat, self.last_lon)

        def get_icon_image(icon_code):
            # OpenWeatherMap icon URL template
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            # Download the icon image
            os.makedirs("icons", exist_ok=True)
            icon_path = os.path.join("icons", f"{icon_code}.png")
            urllib.request.urlretrieve(icon_url, icon_path)
            return tk.PhotoImage(file=icon_path)

        for i in range(5):
            temp_current = int(weather_data["list"][i]["main"]["temp"])
            weather_current_description = weather_data["list"][i]["weather"][0]["description"]
            weather_current_time = weather_data["list"][i]["dt_txt"].split()[1][:5]
            icon_code = weather_data["list"][i]["weather"][0]["icon"]
            icon_image = get_icon_image(icon_code)

            current_time_label = tk.Label(self.main_frame, text=f"{weather_current_time}", bg="#00b4d8", fg="black")
            current_time_label.grid(row=5, column=i, sticky="nsew")
            current_label = tk.Label(self.main_frame, text=f"Temperature: {temp_current}°C", bg="#00b4d8", fg="black")
            current_label.grid(row=6, column=i)
            weather_description_label = tk.Label(self.main_frame,text=f"{weather_current_description.capitalize()}", bg="#00b4d8",fg="black")
            weather_description_label.grid(row=7, column=i)

            label = tk.Label(self.main_frame, image=icon_image, bg="#00b4d8", pady=20)
            label.image = icon_image  # Keep a reference
            label.grid(row=4, column=i)


    def next_page(self):
        weather_data = self.weather.get_weather(self.last_lat, self.last_lon)

        # Clear previously displayed labels in rows 4, 5, 6, 7 and columns 0-4
        for widget in self.main_frame.grid_slaves():
            if int(widget.grid_info()["row"]) in (4, 5, 6, 7) and int(widget.grid_info()["column"]) in range(5):
                widget.destroy()

        def get_icon_image(icon_code):
            # OpenWeatherMap icon URL
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            # Download the icon image
            os.makedirs("icons", exist_ok=True)
            icon_path = os.path.join("icons", f"{icon_code}.png")
            urllib.request.urlretrieve(icon_url, icon_path)
            return tk.PhotoImage(file=icon_path)

        for i in range(5,10):
            temp_current = int(weather_data["list"][i]["main"]["temp"])
            weather_current_description = weather_data["list"][i]["weather"][0]["description"]
            weather_current_time = weather_data["list"][i]["dt_txt"].split()[1][:5]
            icon_code = weather_data["list"][i]["weather"][0]["icon"]
            icon_image = get_icon_image(icon_code)

            current_time_label = tk.Label(self.main_frame, text=f"{weather_current_time}", bg="#00b4d8", fg="black")
            current_time_label.grid(row=5, column=i-5, sticky="nsew")
            current_label = tk.Label(self.main_frame, text=f"Temperature: {temp_current}°C", bg="#00b4d8", fg="black")
            current_label.grid(row=6, column=i-5)
            weather_description_label = tk.Label(self.main_frame, text=f"{weather_current_description.capitalize()}", bg="#00b4d8",
                                                 fg="black")
            weather_description_label.grid(row=7, column=i-5)

            label = tk.Label(self.main_frame, image=icon_image, bg="#00b4d8", pady=20)
            label.image = icon_image  # Keep a reference
            label.grid(row=4, column=i-5)

        self.button_next_page.destroy()
        self.previous_button = tk.Button(self.main_frame,text="Previous",command=self.previous_page,highlightbackground="#00b4d8",
                                          activebackground="#0096c7")
        self.previous_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")


    def previous_page(self):
        self.show_weather()
        self.previous_button.destroy()
        self.button_next_page = tk.Button(self.main_frame, text="Next", command=self.next_page,
                                          highlightbackground="#00b4d8",
                                          activebackground="#0096c7")
        self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

if __name__ == "__main__":
    app = GUI()