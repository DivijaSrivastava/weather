# weather
# 🌤️ WeatherME - Your Weather Companion

A modern, visually appealing desktop weather application built with Python and Tkinter that provides real-time weather information for any location worldwide.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-Open%20Source-brightgreen.svg)

## ✨ Features

- **Real-time Weather Data**: Fetches current weather conditions from wttr.in API
- **Beautiful UI**: Modern dark theme with animated background elements
- **Comprehensive Weather Info**: Displays temperature, humidity, wind speed, pressure, visibility, and more
- **Tomorrow's Forecast**: Shows detailed forecast for the next day including sunrise/sunset times
- **Smooth Animations**: Loading animations and floating background circles
- **Responsive Design**: Scrollable interface to accommodate all weather information
- **User-Friendly**: Intuitive search with enter key support and hover effects

## 📸 Screenshots

### Main Interface
The application features a sleek dark theme with animated background elements and easy-to-use search functionality.

### Weather Display
- Current temperature with weather emoji
- Wind speed and direction
- Humidity levels
- Atmospheric pressure, visibility, cloud cover, and precipitation
- Tomorrow's forecast with sunrise/sunset times

## 📋 Requirements

- Python 3.6 or higher
- Required packages:
  - `tkinter` (usually comes pre-installed with Python)
  - `requests`

## 🚀 Installation

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/weather-pro.git
cd weather-pro
```

### Step 2: Install Dependencies
```bash
pip install requests
```

### Step 3: Run the Application
```bash
python weather_app.py
```

## 💻 Usage

1. **Launch the application**
```bash
   python weather_app.py
```

2. **Enter a city name** in the search box
   - Examples: "London", "New York", "Tokyo", "Paris"

3. **Search for weather**
   - Click the "🔍 Search" button, or
   - Press Enter key

4. **View weather information**:
   - Current temperature and "feels like" temperature
   - Weather description with emoji
   - Wind speed and direction
   - Humidity percentage
   - Atmospheric pressure
   - Visibility
   - Cloud cover
   - Precipitation
   - Tomorrow's forecast with sunrise/sunset times

## 🎨 Features Breakdown

### Current Weather Display
- 🌡️ **Temperature**: Large display with current and "feels like" temperature
- 🌤️ **Weather Condition**: Description with contextual emoji
- 💨 **Wind**: Speed (km/h) with direction (compass point and degrees)
- 💧 **Humidity**: Current humidity percentage
- 🔽 **Pressure**: Atmospheric pressure in millibars
- 👁️ **Visibility**: Visibility range in kilometers
- ☁️ **Cloud Cover**: Cloud coverage percentage
- 🌧️ **Precipitation**: Precipitation amount in millimeters

### Tomorrow's Forecast
- 📅 **Date**: Tomorrow's date
- 🌡️ **Temperature Range**: Maximum and minimum temperatures
- 🌤️ **Weather Condition**: Forecast with emoji
- 🌅 **Sunrise**: Tomorrow's sunrise time
- 🌇 **Sunset**: Tomorrow's sunset time
- 🌧️ **Rain Chance**: Probability of rain
- ☀️ **UV Index**: UV index level

### UI Elements
- ✨ **Animated Background**: Floating circles with smooth motion
- ⏳ **Loading Animation**: Animated dots while fetching data
- 🪟 **Window Controls**: Minimize and close buttons
- 📜 **Scrollable Panel**: Accommodates all weather information
- 🖱️ **Hover Effects**: Interactive buttons with visual feedback
- ⚠️ **Confirmation Dialog**: Prevents accidental closure

## 🌐 API Information

This application uses the **[wttr.in](https://wttr.in)** API:
- Free weather data in JSON format
- No API key required
- Covers worldwide locations
- Provides current conditions and forecasts

**API Endpoint Used:**
```
https://wttr.in/{city}?format=j1
```

## 🎨 Color Scheme

The application uses a modern dark theme with accent colors:

| Element | Color Code | Description |
|---------|-----------|-------------|
| Background | `#0f172a` | Dark blue-grey |
| Cards | `#1e293b` | Lighter dark |
| Accent | `#3b82f6` | Blue |
| Text | `#f1f5f9` | Light grey |
| Wind Card | `#10b981` | Green |
| Humidity Card | `#3b82f6` | Blue |
| Forecast Card | `#f59e0b` | Orange |
| Error Button | `#ef4444` | Red |

## 🔧 Customization

You can customize the appearance by modifying these variables in the `__init__` method:
```python
# Color scheme
self.bg_color = "#0f172a"      # Background color
self.card_color = "#1e293b"     # Card background
self.accent_color = "#3b82f6"   # Accent color (buttons, highlights)
self.text_color = "#f1f5f9"     # Text color
```

### Customizing Window Size
```python
self.root.geometry("600x950")  # Width x Height
```

### Customizing Animation Speed
```python
# In animate_background method
self.root.after(50, self.animate_background)  # Update interval in ms
```

## 📁 Project Structure
```
weather-pro/
│
├── weather_app.py          # Main application file
├── README.md               # This file
└── requirements.txt        # Python dependencies (optional)
```

## 🐛 Troubleshooting

### Issue: City not found
**Solution**: 
- Check spelling and try using a more specific location name
- Try using city name with country (e.g., "Paris, France")
- Ensure the city name is in English

### Issue: Network error
**Solution**: 
- Check your internet connection
- Ensure wttr.in is accessible from your location
- Check if a firewall is blocking the connection

### Issue: Slow loading
**Solution**: 
- This may be due to network latency
- The app will display an error if the request times out after 10 seconds
- Try a different network or check your internet speed

### Issue: Application won't start
**Solution**:
- Ensure Python 3.6+ is installed: `python --version`
- Install required packages: `pip install requests`
- Check if tkinter is installed: `python -m tkinter`

### Issue: Scrolling doesn't work
**Solution**:
- Use mouse wheel to scroll through weather information
- On trackpad, use two-finger scroll gesture

## 🔒 Privacy & Security

- No user data is collected or stored
- All weather data is fetched directly from wttr.in
- No API keys or authentication required
- Application runs entirely on your local machine

## 📝 Notes

- The application requires an active internet connection to fetch weather data
- Weather data is provided by wttr.in and is generally accurate but may occasionally differ from other sources
- The application uses threading to prevent UI freezing during data fetching
- All temperature values are displayed in Celsius (°C)
- Wind speeds are shown in kilometers per hour (km/h)

## 🚀 Future Enhancements

Potential features for future versions:
- [ ] Multiple city weather comparison
- [ ] 7-day forecast
- [ ] Weather alerts and notifications
- [ ] Temperature unit toggle (Celsius/Fahrenheit)
- [ ] Save favorite locations
- [ ] Dark/Light theme toggle
- [ ] Export weather data to CSV
- [ ] Weather maps integration
- [ ] Hourly forecast

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update README if adding new features

## 📄 License

This project is open source and available for personal and educational use.

## 🙏 Acknowledgments

- Weather data provided by [wttr.in](https://wttr.in)
- Built with Python and Tkinter
- Inspired by modern weather applications
- Thanks to the open-source community

## 📞 Contact & Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Questions**: Feel free to ask questions in the Discussions section

## 🌟 Star This Project

If you find this project helpful, please consider giving it a star on GitHub!

---

**Made with ❤️ by Weather Enthusiasts**

**Enjoy tracking the weather with Weather Pro! 🌦️**
