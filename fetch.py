import os
import requests
from sqlalchemy import create_engine, text

# 1️⃣ جلب رابط قاعدة البيانات من متغير البيئة
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("❌ قاعدة البيانات غير معرفة. تأكد من وضع DATABASE_URL في Railway.")

# 2️⃣ إنشاء اتصال بقاعدة البيانات
engine = create_engine(DB_URL)

# 3️⃣ إنشاء الجدول لو مش موجود
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS air_quality (
            id SERIAL PRIMARY KEY,
            city TEXT,
            aqi INTEGER,
            pm25 REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

print("✅ تم التأكد من وجود الجدول air_quality.")

# 4️⃣ جلب بيانات (مثال API وهمي للشرح)
url = "https://api.openaq.org/v2/latest?city=Algiers"  # استبدل API برابطك
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # استخراج بيانات بشكل مبسط
    city = data["results"][0]["city"]
    aqi = 75   # هذا مجرد مثال، غيّره حسب ال API
    pm25 = data["results"][0]["measurements"][0]["value"]

    # 5️⃣ إدخال البيانات داخل الجدول
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO air_quality (city, aqi, pm25)
            VALUES (:city, :aqi, :pm25)
        """), {"city": city, "aqi": aqi, "pm25": pm25})
        conn.commit()

    print(f"✅ تم إدخال البيانات: {city}, AQI={aqi}, PM2.5={pm25}")
else:
    print("❌ فشل في جلب البيانات من API")
