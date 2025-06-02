import tkinter as tk
from tkintermapview import TkinterMapView
from geopy.geocoders import Nominatim

class GUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("800x600")
        self.root.config(background="#00b4d8")
        self.root.title("Weather App")

        self.last_lat = 50.037379
        self.last_lon = 22.005030

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

        self.entry_city = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7",
                                   highlightbackground="#0096c7")
        self.entry_city.grid(row=0, column=1, sticky="ew", padx=(0, 20))

        self.label_enter_zip_code = tk.Label(self.main_frame, text="Enter Zip Code: ", bg="#00b4d8")
        self.label_enter_zip_code.grid(row=0, column=2, sticky="w")

        self.entry_zip_code = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7",
                                       highlightbackground="#0096c7")
        self.entry_zip_code.grid(row=0, column=3, sticky="ew")

        self.label_pick_a_city = tk.Label(self.main_frame, text="Or choose from map", bg="#00b4d8")
        self.label_pick_a_city.grid(row=2, column=0, sticky="w", pady=5)

        self.button_pick_a_city = tk.Button(self.main_frame, text="Pick A City", command=self.open_map,
                                            highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_pick_a_city.grid(row=2, column=1, sticky="w", pady=5)

        self.label_picked_city = tk.Label(self.main_frame, text="", bg="#00b4d8", fg="black")
        self.label_picked_city.grid(row=3, column=0, columnspan=4, sticky="w")


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

        button_close = tk.Button(map_window, text="Close and Save", command=close_map)
        button_close.grid(row=1, column=0, sticky="e", pady=(4, 4), padx=10)

