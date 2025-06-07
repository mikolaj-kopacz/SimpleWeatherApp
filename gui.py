import tkinter as tk
from weather_utils import Weather
from tkintermapview import TkinterMapView
from last_location import LastLocation


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.config(background="#00b4d8")
        self.root.title("Simple Weather App")
        self.icon = tk.PhotoImage(file="icons/icons8-weather-forecast-100.png")
        self.root.iconphoto(True, self.icon)
        self.last_lat = 50.037379
        self.last_lon = 22.005030
        self.weather = Weather()
        self.last_location = LastLocation()
        self.ui_design()
        last_loc = self.last_location.load()
        if last_loc:
            self.last_lat = last_loc["lat"]
            self.last_lon = last_loc["lon"]
            self.city = last_loc.get("city", "")
            self.zipcode = last_loc.get("zipcode", "")
            self.label_picked_city.config(text=f"{self.city} {self.zipcode}".strip())
            self.show_weather()
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

        self.entry_city = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7", fg="black",
                                   highlightbackground="#0096c7")
        self.entry_city.grid(row=0, column=1, sticky="ew", padx=(0, 20))

        self.label_enter_zip_code = tk.Label(self.main_frame, text="Enter Zip Code: ", bg="#00b4d8")
        self.label_enter_zip_code.grid(row=0, column=2, sticky="w")

        self.entry_zip_code = tk.Entry(self.main_frame, bg="#90e0ef", highlightcolor="#0096c7",
                                       highlightbackground="#0096c7", fg="black")
        self.entry_zip_code.grid(row=0, column=3, sticky="ew")

        self.label_pick_a_city = tk.Label(self.main_frame, text="Or choose from map", bg="#00b4d8")
        self.label_pick_a_city.grid(row=2, column=0, sticky="w", pady=5)

        self.button_pick_a_city = tk.Button(self.main_frame, text="Pick A City", command=self.open_map,
                                            highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_pick_a_city.grid(row=2, column=1, sticky="w", pady=5)

        self.label_picked_city = tk.Label(self.main_frame, text="", bg="#00b4d8", fg="black", pady=(50))
        self.label_picked_city.grid(row=3, column=0, columnspan=4, sticky="w")

        self.button_search = tk.Button(self.main_frame, text="Search", command=self.search_for_coords,
                                       highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_search.grid(row=0, column=4, columnspan=4)
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

            location_info = self.weather.get_location_from_coords(lat, lon)
            self.label_picked_city.config(text=location_info["display_text"])
            map_view.set_position(lat, lon)
            city = location_info.get("city", "")
            zipcode = location_info.get("zipcode", "")
            self.last_location.save(city, zipcode, lat, lon)

        map_view.add_left_click_map_command(click)

        def close_map():
            map_window.destroy()
            self.show_weather()

        button_close = tk.Button(map_window, text="Close and Save", command=close_map)
        button_close.grid(row=1, column=0, sticky="e", pady=(4, 4), padx=10)

        self.button_next_page = tk.Button(self.main_frame, text="Next", command=self.next_page,
                                          highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    def search_for_coords(self):
        city_text = self.entry_city.get().strip()
        zip_text = self.entry_zip_code.get().strip()
        self.entry_city.delete(0, "end")
        self.entry_zip_code.delete(0, "end")

        result = self.weather.get_coords_from_query(city_text, zip_text)

        if result["success"]:
            self.last_lat = result["lat"]
            self.last_lon = result["lon"]
            city = result.get("city", "")
            zipcode = result.get("zipcode", "")
            self.city = city
            self.zipcode = zipcode
            self.label_picked_city.config(text=result["display_text"])
            self.show_weather()
            self.last_location.save(city, zipcode, self.last_lat, self.last_lon)

            if hasattr(self, "previous_button") and self.previous_button:
                self.previous_button.destroy()
            self.button_next_page = tk.Button(self.main_frame, text="Next", command=self.next_page,
                                              highlightbackground="#00b4d8", activebackground="#0096c7")
            self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        else:
            self.label_picked_city.config(text=result["error"])

    def clear_weather_display(self):
        for widget in self.main_frame.grid_slaves():
            if int(widget.grid_info()["row"]) in (4, 5, 6, 7) and int(widget.grid_info()["column"]) in range(5):
                widget.destroy()

    def display_weather_data(self, weather_data, start_col=0):
        for i, data in enumerate(weather_data):
            col = start_col + i

            current_time_label = tk.Label(self.main_frame, text=f"{data['time']}", bg="#00b4d8", fg="black")
            current_time_label.grid(row=5, column=col, sticky="nsew")

            current_label = tk.Label(self.main_frame, text=f"Temperature: {data['temperature']}°C",
                                     bg="#00b4d8", fg="black")
            current_label.grid(row=6, column=col)

            weather_description_label = tk.Label(self.main_frame, text=f"{data['description']}",
                                                 bg="#00b4d8", fg="black")
            weather_description_label.grid(row=7, column=col)

            if data['icon_path']:
                icon_image = tk.PhotoImage(file=data['icon_path'])
                label = tk.Label(self.main_frame, image=icon_image, bg="#00b4d8", pady=20)
                label.image = icon_image  # Keep a reference
                label.grid(row=4, column=col)

    def show_weather(self):
        result = self.weather.get_weather_data_for_display(self.last_lat, self.last_lon, 0, 5)

        if result["success"]:
            self.display_weather_data(result["data"])
        else:
            self.label_picked_city.config(text=f"Error: {result.get('error', 'Unknown error')}")

    def next_page(self):
        self.clear_weather_display()

        result = self.weather.get_weather_data_for_display(self.last_lat, self.last_lon, 5, 5)

        if result["success"]:
            self.display_weather_data(result["data"])

        self.button_next_page.destroy()
        self.previous_button = tk.Button(self.main_frame, text="Previous", command=self.previous_page,
                                         highlightbackground="#00b4d8", activebackground="#0096c7")
        self.previous_button.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    def previous_page(self):
        self.clear_weather_display()

        self.show_weather()

        self.previous_button.destroy()
        self.button_next_page = tk.Button(self.main_frame, text="Next", command=self.next_page,
                                          highlightbackground="#00b4d8", activebackground="#0096c7")
        self.button_next_page.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")


if __name__ == "__main__":
    app = GUI()