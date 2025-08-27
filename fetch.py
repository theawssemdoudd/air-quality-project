import requests
import pandas as pd
import os
import schedule
import time
from datetime import datetime

API_TOKEN = os.getenv("AQI_TOKEN")  # التوكن من متغير البيئة
CITY = "beijing"

def fetch_data():
    print(f"[{datetime.now()}] Fetching AQI data for {CITY}...")
    url = f"https://api.waqi.info/feed/{CITY}/?token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        print("Error fetching data:", data)
        return

    iaqi = data["data"]["iaqi"]
    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aqi": data["data"]["aqi"],
        **{k: v["v"] for k, v in iaqi.items()}
    }

    # حفظ في CSV
    os.makedirs("data", exist_ok=True)
    file_path = "data/air_quality.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])

    df.to_csv(file_path, index=False)
    print(f"✅ Data saved to {file_path}")

# تشغيل كل ساعة
schedule.every(1).hours.do(fetch_data)

print("🚀 Service started... Collecting AQI data every hour.")

# حلقة مستمرة حتى يوقفها Railway (service يعمل 24/7)
while True:
    schedule.run_pending()
    time.sleep(60)
