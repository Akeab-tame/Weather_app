from flask import Flask, render_template, request, redirect, url_for

import requests
import sqlite3

app = Flask(__name__)

# OpenWeather API key and base URL for fetching weather data
API_KEY = '3aa195e7e0d2c6739f5759b5696d6f96'
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

# YouTube API key and base URL for fetching travel-related videos
YOUTUBE_API_KEY = 'AIzaSyB-1EK-pTcBbCXSmbdVfKGtSU7E8qpuVHI'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'


# Function to initialize the SQLite database and create a table for storing weather data
def init_db():
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            city TEXT,
                            date TEXT,
                            temperature REAL,
                            description TEXT
                          )''')
        conn.commit()


# Route to render the home page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch weather data based on user input and display results
@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']   # Retrieve city name from form input

    # Construct API URLs for current weather and forecast data
    current_url = f'{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric'
    forecast_url = f'{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric'


    # Fetch current weather and forecast data from OpenWeather API
    current_response = requests.get(current_url).json()
    forecast_response = requests.get(forecast_url).json()
    
    # Check if the city was found, otherwise return an error message
    if current_response.get('cod') != 200:
        return render_template('index.html', error="City not found.")

    # Extract relevant weather details
    weather_data = {
        'city': city,
        'temperature': current_response['main']['temp'],
        'description': current_response['weather'][0]['description'],
        'humidity': current_response['main']['humidity'],
        'wind_speed': current_response['wind']['speed'],
        'icon': current_response['weather'][0]['icon'],
    }

    # Extract forecast details for multiple timestamps
    forecast_data = []
    for entry in forecast_response['list']:
        forecast_data.append({
            'date': entry['dt_txt'],
            'temperature': entry['main']['temp'],
            'description': entry['weather'][0]['description'],
            'icon': entry['weather'][0]['icon']
        })

    # Store forecast data in the SQLite database
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        for entry in forecast_data:
            cursor.execute("INSERT INTO weather (city, date, temperature, description) VALUES (?, ?, ?, ?)",
                           (city, entry['date'], entry['temperature'], entry['description']))
        conn.commit()
    
    # Fetch YouTube videos related to the city
    youtube_params = {
        'part': 'snippet',
        'q': f'{city} travel',
        'key': YOUTUBE_API_KEY,
        'maxResults': 5     # Limit results to 5 videos
    }
    youtube_response = requests.get(YOUTUBE_SEARCH_URL, params=youtube_params).json()
    
    # Extract video details such as title, video ID, and thumbnail
    videos = []
    for item in youtube_response.get('items', []):
        if 'videoId' in item['id']:
            videos.append({
                'title': item['snippet']['title'],
                'videoId': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            })
    
    # Render the result page with weather, forecast, and YouTube video data
    return render_template('result.html', weather=weather_data, forecast=forecast_data, videos=videos)

# Route to display the weather history stored in the database
@app.route('/history')
def history():
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather")  # Retrieve all records
        history_data = cursor.fetchall()   # Fetch all data
    return render_template('history.html', history=history_data)


# Route to delete a specific entry from the weather history based on its ID
@app.route('/delete/<int:id>')
def delete_entry(id):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather WHERE id = ?", (id,))  # Delete record by ID
        conn.commit()
    return redirect(url_for('history'))    # Redirect back to the history page


# Run the Flask application
if __name__ == '__main__':
    init_db()
    app.run(debug=True)