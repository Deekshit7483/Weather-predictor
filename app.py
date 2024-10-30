from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS

API_KEY = '1557188db531c9a1265201eee47ee0d8'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/onecall'

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    # Get the current weather to find the coordinates
    current_weather_response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'q': city, 'appid': API_KEY, 'units': 'metric'}
    )
    
    if current_weather_response.status_code != 200:
        return jsonify({'error': 'City not found or API limit reached.'}), 404
    
    current_weather = current_weather_response.json()
    lat = current_weather['coord']['lat']
    lon = current_weather['coord']['lon']
    
    # Get historical and forecasted weather
    one_call_response = requests.get(
        BASE_URL,
        params={
            'lat': lat,
            'lon': lon,
            'exclude': 'minutely',
            'appid': API_KEY,
            'units': 'metric'
        }
    )
    
    if one_call_response.status_code != 200:
        return jsonify({'error': 'Error fetching weather data.'}), 500
    
    data = one_call_response.json()
    
    # Get current weather data
    current_data = {
        'temperature': data['current']['temp'],
        'humidity': data['current']['humidity'],
        'description': data['current']['weather'][0]['description']
    }
    
    # Create time series data for the last 7 days
    time_series = []
    for day in data['daily'][:7]:
        date = datetime.utcfromtimestamp(day['dt']).strftime('%Y-%m-%d')
        time_series.append({
            'date': date,
            'temperature': day['temp']['day'],
            'humidity': day['humidity']
        })
    
    return jsonify({
        'current': current_data,
        'time_series': time_series
    })

if __name__ == "__main__":
    app.run(debug=True)
