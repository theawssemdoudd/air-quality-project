import requests
import pandas as pd
import os
from datetime import datetime

API_TOKEN = os.getenv("AQI_TOKEN")  # نخزن التوكن كمتغير بيئة

cities = ["beijing", "paris", "algiers"]

def fetch_city(city):
    url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"
    r = requests.get(url).json()
    if r["status"] == "ok":
        data = r["data"]
        record = {
            "city": city,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "aqi": data.get("aqi"),
        }
        for k, v in data["iaqi"].items():
            record[k] = v.get("v")
        return record
    return None

all_data = [fetch_city(c) for c in cities]
df = pd.DataFrame([d for d in all_data if d])

csv_file = "air_quality.csv"

# حفظ البيانات مع append
if os.path.exists(csv_file):
    df.to_csv(csv_file, mode="a", header=False, index=False)
else:
    df.to_csv(csv_file, index=False)

print("Data collected and saved successfully!")
