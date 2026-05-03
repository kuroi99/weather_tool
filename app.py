from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

cities = ["Kuwana, JP", "Suwa,JP", "Kashiwa,JP"]

@app.route("/")
def index():
    weather_data =[]

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"
        response = requests.get(url)
        data = response.json()

        forecasts = []
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja&cnt=5"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        for item in forecast_data['list']:
            utc_time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
            jst_time = utc_time + timedelta(hours=9)
            forecasts.append({
                'time' : jst_time.strftime("%Y-%m-%d %H:%M"),
                'description' : item["weather"][0]['description'],
                'temp': item['main']['temp'],
                'is_rain' : 'rain' in item['weather'][0]['main'].lower() or '雨' in item['weather'][0]['description']
            })

        weather_data.append({
            'name' : data['name'],
            'description' : data['weather'][0]['description'],
            'temp' : data['main']['temp'],
            'feels_like' : data['main']['feels_like'],
            'humidity' : data['main']['humidity'],
            'forecasts' : forecasts
        })

    return render_template("index.html", weather_data=weather_data)

@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")
    arrival_time = request.form.get("arrival_time")

    arrival_dt = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M")

    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja&cnt=40"
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    closest = None
    min_diff = None

    for item in forecast_data['list']:
        utc_time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
        jst_time = utc_time + timedelta(hours=9)
        diff = abs((jst_time - arrival_dt).total_seconds())
        if min_diff is None or diff < min_diff:
            min_diff = diff
            closest = {
                'city': forecast_data['city']['name'],
                'time': jst_time.strftime('%Y-%m-%d %H:%M'),
                'description': item['weather'][0]['description'],
                'temp': item['main']['temp'],
                'is_rain': 'rain' in item['weather'][0]['main'].lower() or '雨' in item['weather'][0]['description']
            }

    return render_template("search_result.html", result=closest, arrival_time=arrival_dt.strftime('%Y-%m-%d %H:%M'))
    
if __name__ == "__main__":
    app.run(debug=True)