import os
import pandas as pd
from sqlalchemy import create_engine

# خزن رابط قاعدة البيانات كمتغير بيئة في Railway (DATABASE_URL)
DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("❌ قاعدة البيانات غير معرفة. تأكد من وضع DATABASE_URL في Railway.")

# إنشاء الاتصال
engine = create_engine(DB_URL, echo=True)

# مثال: إنشاء جدول
df = pd.DataFrame({"city": ["Beijing"], "aqi": [46]})
df.to_sql("air_quality", engine, if_exists="append", index=False)

print("✅ تم الحفظ في PostgreSQL بنجاح!")
