# Flask Weather App  

A simple Flask-based web application that fetches the current weather and a 5-day forecast for any city using the OpenWeather API. It also integrates YouTube videos related to the searched city for travel recommendations.  

## 🚀 Features  
- Fetches **current weather details** (temperature, humidity, wind speed, description, etc.).  
- Displays a **5-day forecast** with detailed weather conditions.  
- Stores weather history in an **SQLite database** for future reference.  
- Integrates **YouTube travel videos** related to the searched city.  
- Provides an option to **delete past weather records**.  

## 🛠️ Setup  

1. **Clone the repository:**  
```bash
   git clone https://github.com/Akeab-tame/weather-app.git
   cd weather-app
```

2. **Create a virtual environment:**  
```bash
   python -m venv venv
   source ./venv/Scripts/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**  
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables** (optional, for security purposes):  
   - Replace API keys directly in `app.py` or create a `.env` file and load them using `dotenv`.

5. **Run the application:**  
   ```bash
   python app.py
   ```

6. **Open in your browser:**  
   Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).  

## 📌 API Integration  
- **Weather Data:** OpenWeather API  
- **YouTube Videos:** YouTube Data API v3  


## 🔥 Next Steps  
- **Improve UI:** Add animations, better color schemes, and responsive design.  
- **Enhance Data Presentation:** Display forecasts as an interactive graph using Chart.js.  
- **Expand Features:** Add more weather insights such as UV index, sunrise/sunset time, and air quality.  
- **User Authentication:** Allow users to save favorite locations and view past searches.  


