from datetime import datetime, timedelta
import requests 
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

cities = ["Kuwana,JP", "Suwa,JP", "Kashiwa,JP"]


for city in cities:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ja"      
    response = requests.get(url)
    data = response.json()
    print(f"\n== {data['name']} ==")
    print(f"天気: {data['weather'][0]['description']}")
    print(f"気温: {data['main']['temp']}°C")
    print(f"体感気温: {data['main']['feels_like']}°C")
    print(f"湿度: {data['main']['humidity']}%")

print("\n---予報---")

for city in cities:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja&cnt=5"

    response = requests.get(url)
    data = response.json()
    # jsonデータが見にくい時インデントを揃えて見やすくできる
    # from pprint import pprint
    # pprint(data)
    print(f"\n== {data['city']['name']} ==")
    for item in data['list']:
        utc_time = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
        jst_time = utc_time + timedelta(hours=9)
        print(f"\n日時 : {jst_time.strftime('%Y-%m-%d %H:%M')} (JST)")
        print(f"天気 : {item['weather'][0]['description']}")
        print(f"気温 : {item['main']['temp']}°C")
        if "rain" in item['weather'][0]['main'].lower() or '雨' in item['weather'][0]['description']:
            print(f" ⚠️ 雨の予報があります！")