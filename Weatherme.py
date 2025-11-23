import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
from datetime import datetime
import math

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Pro - Your Weather Companion")
        self.root.geometry("600x950")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_color = "#0f172a"  # Dark blue-grey
        self.card_color = "#1e293b"  # Lighter dark
        self.accent_color = "#3b82f6"  # Blue
        self.text_color = "#f1f5f9"
        
        # Animation variables
        self.loading = False
        self.dot_count = 0
        self.circle_angle = 0
        self.circles = []
        self.animation_running = True
        
        # Remove window decorations for modern look
        self.root.overrideredirect(False)
        
        self.create_animated_background()
        self.create_widgets()
        self.animate_background()
        
    def create_animated_background(self):
        """Create animated background canvas"""
        self.bg_canvas = tk.Canvas(
            self.root,
            bg=self.bg_color,
            highlightthickness=0,
            width=600,
            height=950
        )
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create floating circles for animation
        for i in range(8):
            x = (i % 4) * 150 + 75
            y = (i // 4) * 475 + 100
            circle = self.bg_canvas.create_oval(
                x-30, y-30, x+30, y+30,
                fill="",
                outline="#1e3a8a",
                width=2
            )
            self.circles.append({
                'id': circle,
                'x': x,
                'y': y,
                'radius': 30,
                'angle': i * 45
            })
    
    def animate_background(self):
        """Animate background circles"""
        if not self.animation_running:
            return
            
        for circle in self.circles:
            circle['angle'] += 0.5
            offset_x = math.sin(math.radians(circle['angle'])) * 10
            offset_y = math.cos(math.radians(circle['angle'])) * 10
            
            x = circle['x'] + offset_x
            y = circle['y'] + offset_y
            r = circle['radius']
            
            self.bg_canvas.coords(
                circle['id'],
                x - r, y - r, x + r, y + r
            )
        
        self.root.after(50, self.animate_background)
    
    def create_widgets(self):
        # Main container frame
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.place(relx=0.5, rely=0.5, anchor="center", width=560, height=920)
        
        # Top bar with title and close button
        top_bar = tk.Frame(main_container, bg=self.card_color, height=60)
        top_bar.pack(fill="x", pady=(0, 10))
        top_bar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            top_bar,
            text="🌤️ Weather Pro",
            font=("Helvetica", 24, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )
        title_label.pack(side="left", padx=20, pady=10)
        
        # Minimize and Close buttons
        button_frame = tk.Frame(top_bar, bg=self.card_color)
        button_frame.pack(side="right", padx=10)
        
        minimize_btn = tk.Button(
            button_frame,
            text="—",
            font=("Helvetica", 14, "bold"),
            bg=self.card_color,
            fg="#fbbf24",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.minimize_window,
            width=3,
            height=1
        )
        minimize_btn.pack(side="left", padx=2)
        minimize_btn.bind("<Enter>", lambda e: minimize_btn.config(bg="#374151"))
        minimize_btn.bind("<Leave>", lambda e: minimize_btn.config(bg=self.card_color))
        
        close_btn = tk.Button(
            button_frame,
            text="✕",
            font=("Helvetica", 14, "bold"),
            bg=self.card_color,
            fg="#ef4444",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.quit_app,
            width=3,
            height=1
        )
        close_btn.pack(side="left", padx=2)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#ef4444", fg="white"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=self.card_color, fg="#ef4444"))
        
        # Content frame with scrollable area
        content_frame = tk.Frame(main_container, bg=self.bg_color)
        content_frame.pack(fill="both", expand=True)
        
        # Subtitle
        subtitle = tk.Label(
            content_frame,
            text="Get real-time weather for any location",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg="#94a3b8"
        )
        subtitle.pack(pady=(5, 15))
        
        # Search frame
        search_frame = tk.Frame(content_frame, bg=self.card_color, height=70)
        search_frame.pack(fill="x", padx=20, pady=10)
        search_frame.pack_propagate(False)
        
        search_inner = tk.Frame(search_frame, bg=self.card_color)
        search_inner.pack(expand=True, fill="both", padx=15, pady=10)
        
        # Entry with modern style
        entry_frame = tk.Frame(search_inner, bg="#0f172a", relief="flat", bd=1)
        entry_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.city_entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 14),
            bg="#0f172a",
            fg=self.text_color,
            relief="flat",
            bd=0,
            insertbackground=self.accent_color
        )
        self.city_entry.pack(fill="both", expand=True, padx=10, pady=8)
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind("<FocusIn>", self.on_entry_click)
        self.city_entry.bind("<FocusOut>", self.on_focusout)
        self.city_entry.bind("<Return>", lambda e: self.search_weather())
        
        # Search button
        self.search_btn = tk.Button(
            search_inner,
            text="🔍 Search",
            font=("Helvetica", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.search_weather,
            padx=25,
            pady=10
        )
        self.search_btn.pack(side="right")
        self.search_btn.bind("<Enter>", self.on_button_hover)
        self.search_btn.bind("<Leave>", self.on_button_leave)
        
        # Loading label
        self.loading_label = tk.Label(
            content_frame,
            text="",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.loading_label.pack(pady=5)
        
        # Scrollable weather display frame
        canvas_frame = tk.Frame(content_frame, bg=self.bg_color)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.weather_canvas = tk.Canvas(canvas_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.weather_canvas.yview)
        self.weather_frame = tk.Frame(self.weather_canvas, bg=self.bg_color)
        
        self.weather_frame.bind(
            "<Configure>",
            lambda e: self.weather_canvas.configure(scrollregion=self.weather_canvas.bbox("all"))
        )
        
        self.weather_canvas.create_window((0, 0), window=self.weather_frame, anchor="nw")
        self.weather_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.weather_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel for scrolling
        self.weather_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Quit button at bottom
        quit_btn = tk.Button(
            main_container,
            text="🚪 Quit Application",
            font=("Helvetica", 12, "bold"),
            bg="#ef4444",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.quit_app,
            pady=12
        )
        quit_btn.pack(fill="x", padx=20, pady=(10, 0))
        quit_btn.bind("<Enter>", lambda e: quit_btn.config(bg="#dc2626"))
        quit_btn.bind("<Leave>", lambda e: quit_btn.config(bg="#ef4444"))
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.weather_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def minimize_window(self):
        """Minimize the window"""
        self.root.iconify()
    
    def quit_app(self):
        """Quit the application with confirmation"""
        if messagebox.askokcancel("Quit", "Do you want to quit Weather Pro?"):
            self.animation_running = False
            self.root.quit()
            self.root.destroy()
    
    def on_entry_click(self, event):
        if self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, "end")
            self.city_entry.config(fg=self.text_color)
    
    def on_focusout(self, event):
        if self.city_entry.get() == "":
            self.city_entry.insert(0, "Enter city name...")
            self.city_entry.config(fg="#64748b")
    
    def on_button_hover(self, event):
        self.search_btn.config(bg="#2563eb")
    
    def on_button_leave(self, event):
        self.search_btn.config(bg=self.accent_color)
    
    def animate_loading(self):
        if self.loading:
            dots = "." * (self.dot_count % 4)
            self.loading_label.config(text=f"Fetching weather data{dots}")
            self.dot_count += 1
            self.root.after(300, self.animate_loading)
    
    def search_weather(self):
        city = self.city_entry.get()
        if city == "" or city == "Enter city name...":
            messagebox.showwarning("Input Error", "Please enter a city name!")
            return
        
        self.loading = True
        self.dot_count = 0
        self.animate_loading()
        
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        thread = threading.Thread(target=self.fetch_weather, args=(city,))
        thread.daemon = True
        thread.start()
    
    def fetch_weather(self, city):
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.root.after(0, lambda: self.display_weather(data))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
        finally:
            self.loading = False
            self.root.after(0, lambda: self.loading_label.config(text=""))
    
    def show_error(self, error_msg):
        self.loading_label.config(text="")
        messagebox.showerror("Error", f"Unable to fetch weather data.\n{error_msg}")
    
    def display_weather(self, data):
        try:
            current = data['current_condition'][0]
            location = data['nearest_area'][0]
            
            self.loading_label.config(text="")
            
            # Location card
            location_card = tk.Frame(self.weather_frame, bg=self.card_color, relief="flat")
            location_card.pack(fill="x", pady=10)
            
            location_name = tk.Label(
                location_card,
                text=f"📍 {location['areaName'][0]['value']}, {location['country'][0]['value']}",
                font=("Helvetica", 18, "bold"),
                bg=self.card_color,
                fg=self.text_color,
                pady=15
            )
            location_name.pack()
            
            # Temperature card
            temp_card = tk.Frame(self.weather_frame, bg=self.accent_color, relief="flat")
            temp_card.pack(fill="x", pady=10)
            
            weather_desc = current['weatherDesc'][0]['value'].lower()
            emoji = self.get_weather_emoji(weather_desc)
            
            emoji_label = tk.Label(
                temp_card,
                text=emoji,
                font=("Helvetica", 60),
                bg=self.accent_color,
                pady=10
            )
            emoji_label.pack()
            
            temp_label = tk.Label(
                temp_card,
                text=f"{current['temp_C']}°C",
                font=("Helvetica", 48, "bold"),
                bg=self.accent_color,
                fg="white"
            )
            temp_label.pack()
            
            feels_label = tk.Label(
                temp_card,
                text=f"Feels like {current['FeelsLikeC']}°C",
                font=("Helvetica", 14),
                bg=self.accent_color,
                fg="white",
                pady=5
            )
            feels_label.pack()
            
            desc_label = tk.Label(
                temp_card,
                text=current['weatherDesc'][0]['value'],
                font=("Helvetica", 16),
                bg=self.accent_color,
                fg="white",
                pady=10
            )
            desc_label.pack()
            
            # Wind and Humidity highlights
            highlight_frame = tk.Frame(self.weather_frame, bg=self.bg_color)
            highlight_frame.pack(fill="x", pady=10)
            
            wind_card = tk.Frame(highlight_frame, bg="#10b981", relief="flat")
            wind_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
            
            tk.Label(wind_card, text="💨", font=("Helvetica", 36), bg="#10b981").pack(pady=(15, 5))
            tk.Label(wind_card, text="Wind Speed", font=("Helvetica", 12), bg="#10b981", fg="white").pack()
            tk.Label(wind_card, text=f"{current['windspeedKmph']} km/h", font=("Helvetica", 20, "bold"), bg="#10b981", fg="white").pack()
            tk.Label(wind_card, text=f"{current['winddir16Point']} ({current['winddirDegree']}°)", font=("Helvetica", 10), bg="#10b981", fg="white").pack(pady=(0, 15))
            
            humidity_card = tk.Frame(highlight_frame, bg="#3b82f6", relief="flat")
            humidity_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
            
            tk.Label(humidity_card, text="💧", font=("Helvetica", 36), bg="#3b82f6").pack(pady=(15, 5))
            tk.Label(humidity_card, text="Humidity", font=("Helvetica", 12), bg="#3b82f6", fg="white").pack()
            tk.Label(humidity_card, text=f"{current['humidity']}%", font=("Helvetica", 20, "bold"), bg="#3b82f6", fg="white").pack(pady=(0, 15))
            
            # Details grid
            details_frame = tk.Frame(self.weather_frame, bg=self.bg_color)
            details_frame.pack(fill="both", pady=10)
            
            details = [
                ("🔽", "Pressure", f"{current['pressure']} mb"),
                ("👁️", "Visibility", f"{current['visibility']} km"),
                ("☁️", "Cloud Cover", f"{current['cloudcover']}%"),
                ("🌧️", "Precipitation", f"{current['precipMM']} mm")
            ]
            
            row, col = 0, 0
            for emoji, label, value in details:
                detail_card = tk.Frame(details_frame, bg=self.card_color, relief="flat")
                detail_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                
                tk.Label(detail_card, text=emoji, font=("Helvetica", 24), bg=self.card_color).pack(pady=(10, 0))
                tk.Label(detail_card, text=label, font=("Helvetica", 10), bg=self.card_color, fg="#94a3b8").pack()
                tk.Label(detail_card, text=value, font=("Helvetica", 14, "bold"), bg=self.card_color, fg=self.text_color).pack(pady=(0, 10))
                
                col += 1
                if col > 1:
                    col, row = 0, row + 1
            
            for i in range(2):
                details_frame.grid_rowconfigure(i, weight=1)
                details_frame.grid_columnconfigure(i, weight=1)
            
            self.display_tomorrow_forecast(data)
            
        except KeyError as e:
            self.show_error(f"Unable to parse weather data: {e}")
    
    def display_tomorrow_forecast(self, data):
        try:
            tomorrow = data['weather'][1]
            
            tk.Label(self.weather_frame, text="📅 Tomorrow's Forecast", font=("Helvetica", 18, "bold"), bg=self.bg_color, fg=self.text_color, pady=10).pack()
            
            forecast_card = tk.Frame(self.weather_frame, bg="#f59e0b", relief="flat")
            forecast_card.pack(fill="x", pady=10)
            
            tk.Label(forecast_card, text=tomorrow['date'], font=("Helvetica", 14), bg="#f59e0b", fg="white", pady=10).pack()
            
            tomorrow_desc = tomorrow['hourly'][4]['weatherDesc'][0]['value']
            tomorrow_emoji = self.get_weather_emoji(tomorrow_desc.lower())
            
            tk.Label(forecast_card, text=tomorrow_emoji, font=("Helvetica", 40), bg="#f59e0b").pack()
            tk.Label(forecast_card, text=tomorrow_desc, font=("Helvetica", 14), bg="#f59e0b", fg="white").pack()
            
            temp_frame = tk.Frame(forecast_card, bg="#f59e0b")
            temp_frame.pack(pady=10)
            
            tk.Label(temp_frame, text=f"Max: {tomorrow['maxtempC']}°C", font=("Helvetica", 16, "bold"), bg="#f59e0b", fg="white").pack(side="left", padx=20)
            tk.Label(temp_frame, text=f"Min: {tomorrow['mintempC']}°C", font=("Helvetica", 16, "bold"), bg="#f59e0b", fg="white").pack(side="right", padx=20)
            
            details_frame = tk.Frame(forecast_card, bg="#f59e0b")
            details_frame.pack(fill="x", padx=20, pady=10)
            
            sunrise = tomorrow['astronomy'][0]['sunrise']
            sunset = tomorrow['astronomy'][0]['sunset']
            
            sun_frame = tk.Frame(details_frame, bg="#f59e0b")
            sun_frame.pack(fill="x", pady=5)
            
            tk.Label(sun_frame, text=f"🌅 Sunrise: {sunrise}", font=("Helvetica", 12), bg="#f59e0b", fg="white").pack(side="left")
            tk.Label(sun_frame, text=f"🌇 Sunset: {sunset}", font=("Helvetica", 12), bg="#f59e0b", fg="white").pack(side="right")
            
            tk.Label(details_frame, text=f"🌧️ Chance of Rain: {tomorrow['hourly'][4]['chanceofrain']}%", font=("Helvetica", 12), bg="#f59e0b", fg="white", pady=5).pack()
            tk.Label(details_frame, text=f"☀️ UV Index: {tomorrow['uvIndex']}", font=("Helvetica", 12), bg="#f59e0b", fg="white", pady=(0, 10)).pack()
            
        except (KeyError, IndexError) as e:
            print(f"Error displaying forecast: {e}")
    
    def get_weather_emoji(self, description):
        if "clear" in description or "sunny" in description:
            return "☀️"
        elif "cloud" in description:
            return "☁️"
        elif "rain" in description:
            return "🌧️"
        elif "snow" in description:
            return "❄️"
        elif "thunder" in description or "storm" in description:
            return "⛈️"
        elif "fog" in description or "mist" in description:
            return "🌫️"
        else:
            return "🌤️"

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
