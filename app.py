from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your OpenWeather API key
API_KEY = '3aa195e7e0d2c6739f5759b5696d6f96'
BASE_URL = 'http://api.openweathermap.org/data/2.5/'

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
    
    return render_template('result.html', weather=weather_data, forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)