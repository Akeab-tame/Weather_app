from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3

app = Flask(__name__)

# Replace with your OpenWeather API key
API_KEY = '3aa195e7e0d2c6739f5759b5696d6f96'
BASE_URL = 'http://api.openweathermap.org/data/2.5/'
# Replace with your youtube API key
YOUTUBE_API_KEY = 'AIzaSyB-1EK-pTcBbCXSmbdVfKGtSU7E8qpuVHI'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

# Database setup
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    current_url = f'{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric'
    forecast_url = f'{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric'

    current_response = requests.get(current_url).json()
    forecast_response = requests.get(forecast_url).json()

    if current_response.get('cod') != 200:
        return render_template('index.html', error="City not found.")

    weather_data = {
        'city': city,
        'temperature': current_response['main']['temp'],
        'description': current_response['weather'][0]['description'],
        'humidity': current_response['main']['humidity'],
        'wind_speed': current_response['wind']['speed'],
        'icon': current_response['weather'][0]['icon'],
    }

    forecast_data = []
    for entry in forecast_response['list']:
        forecast_data.append({
            'date': entry['dt_txt'],
            'temperature': entry['main']['temp'],
            'description': entry['weather'][0]['description'],
            'icon': entry['weather'][0]['icon']
        })

    # Store in database
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
        'maxResults': 5
    }
    youtube_response = requests.get(YOUTUBE_SEARCH_URL, params=youtube_params).json()
    videos = []
    for item in youtube_response.get('items', []):
        if 'videoId' in item['id']:
            videos.append({
                'title': item['snippet']['title'],
                'videoId': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            })
    
    return render_template('result.html', weather=weather_data, forecast=forecast_data, videos=videos)

@app.route('/history')
def history():
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather")
        history_data = cursor.fetchall()
    return render_template('history.html', history=history_data)

@app.route('/delete/<int:id>')
def delete_entry(id):
    with sqlite3.connect("weather.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weather WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('history'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)