import requests
import pandas as pd
import os
import schedule
import time
from datetime import datetime
from sqlalchemy import create_engine

# متغيرات البيئة
API_TOKEN = os.getenv("AQI_TOKEN")
DB_URL = os.getenv("DATABASE_URL")  # من Railway (Postgres)

CITY = "beijing"

# إنشاء اتصال مع PostgreSQL
engine = create_engine(DB_URL)

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

    # تحويل إلى DataFrame
    df = pd.DataFrame([record])

    # حفظ في PostgreSQL
    df.to_sql("air_quality", engine, if_exists="append", index=False)
    print("✅ Data saved to PostgreSQL")

# تشغيل كل ساعة
schedule.every(1).hours.do(fetch_data)

print("🚀 Service started... Collecting AQI data every hour.")

while True:
    schedule.run_pending()
    time.sleep(60)
