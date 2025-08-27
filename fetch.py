import requests
import pandas as pd
import os
import schedule
import time
from datetime import datetime
from sqlalchemy import create_engine

# ----------------------------
# متغيرات البيئة (من Railway)
# ----------------------------
API_TOKEN = os.getenv("AQI_TOKEN")
DB_URL = os.getenv("DATABASE_URL")  # PostgreSQL من Railway

CITY = "beijing"

if not API_TOKEN:
    raise ValueError("❌ API Token غير موجود. ضع AQI_TOKEN في متغيرات Railway.")

if not DB_URL:
    raise ValueError("❌ قاعدة البيانات غير معرفة. ضع DATABASE_URL من Postgres Plugin في متغيرات Railway.")

# ----------------------------
# إنشاء اتصال مع PostgreSQL
# ----------------------------
engine = create_engine(DB_URL)

def fetch_data():
    print(f"[{datetime.now()}] Fetching AQI data for {CITY}...")

    url = f"https://api.waqi.info/feed/{CITY}/?token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("⚠️ Error fetching data:", data)
        return

    iaqi = data["data"]["iaqi"]

    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aqi": data["data"].get("aqi"),
        **{k: v["v"] for k, v in iaqi.items()}
    }

    # تحويل إلى DataFrame
    df = pd.DataFrame([record])

    # حفظ في PostgreSQL
    df.to_sql("air_quality", engine, if_exists="append", index=False)
    print("✅ Data saved to PostgreSQL")

# ----------------------------
# جدولة التشغيل
# ----------------------------
schedule.every(1).hours.do(fetch_data)

print("🚀 Service started... Collecting AQI data every hour.")

# ----------------------------
# حلقة تشغيل مستمرة
# ----------------------------
while True:
    schedule.run_pending()
    time.sleep(60)
