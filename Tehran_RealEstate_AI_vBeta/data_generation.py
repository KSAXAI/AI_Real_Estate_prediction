import sqlite3
import random

# اتصال به پایگاه داده SQLite (در صورت عدم وجود، ایجاد می‌کند)
conn = sqlite3.connect('realestate.db')
cursor = conn.cursor()

# ایجاد جدول realestate در صورت عدم وجود
cursor.execute('''
CREATE TABLE IF NOT EXISTS realestate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT,
    area REAL,
    rooms INTEGER,
    bathrooms INTEGER,
    floor INTEGER,
    year_built INTEGER,
    parking INTEGER,
    price REAL
)
''')

# دیکشنری شامل 22 منطقه تهران با فاکتور کیفیت برای شبیه‌سازی تفاوت‌های قیمتی
districts = {
    'منطقه_1': 1.30,
    'منطقه_2': 1.28,
    'منطقه_3': 1.25,
    'منطقه_4': 1.22,
    'منطقه_5': 1.20,
    'منطقه_6': 1.18,
    'منطقه_7': 1.15,
    'منطقه_8': 1.12,
    'منطقه_9': 1.10,
    'منطقه_10': 1.08,
    'منطقه_11': 1.05,
    'منطقه_12': 1.03,
    'منطقه_13': 1.00,
    'منطقه_14': 0.98,
    'منطقه_15': 0.96,
    'منطقه_16': 0.94,
    'منطقه_17': 0.92,
    'منطقه_18': 0.90,
    'منطقه_19': 0.88,
    'منطقه_20': 0.86,
    'منطقه_21': 0.84,
    'منطقه_22': 0.82
}

# بررسی تعداد رکوردها؛ اگر از قبل ۱۰۰۰ یا بیشتر رکورد وجود داشته باشد، اسکریپت متوقف می‌شود.
cursor.execute('SELECT COUNT(*) FROM realestate')
count = cursor.fetchone()[0]
if count >= 1000:
    print("پایگاه داده دارای 1000 یا بیشتر رکورد است.")
    conn.close()
    exit()

# تولید ۱۰۰۰ رکورد واقع‌گرایانه
records = []
for i in range(1000):
    # انتخاب تصادفی یک منطقه از 22 منطقه تهران
    district = random.choice(list(districts.keys()))
    quality_factor = districts[district]
    
    # تولید ویژگی‌های ملک:
    # - مساحت بین 30 تا 250 متر مربع
    area = round(random.uniform(30.0, 250.0), 1)
    # - تعداد اتاق از 1 تا 6
    rooms = random.randint(1, 6)
    # - تعداد حمام از 1 تا 3
    bathrooms = random.randint(1, 3)
    # - شماره طبقه بین 1 تا 20 (با فرض ساختمان‌های آپارتمانی)
    floor = random.randint(1, 20)
    # - سال ساخت در محدوده 1370 تا 1400 (مثال: سال‌های خورشیدی)
    year_built = random.randint(1370, 1400)
    # - تعداد پارکینگ از 0 تا 2
    parking = random.randint(0, 2)
    
    # محاسبه قیمت ملک:
    # قیمت پایه: مساحت * 5,000,000 تومان ضربدر فاکتور منطقه
    base_price = area * 50000000 * quality_factor
    # اضافه‌کردن مزایا براساس تعداد اتاق، حمام و پارکینگ
    extras = rooms * 200000000 + bathrooms * 150000000 + parking * 100000000
    # اعمال استهلاک: هر سال قدیمی‌تر ساختمان باعث کاهش قیمت می‌شود
    depreciation = (1404 - year_built) * 50000000
    # افزودن نوسان تصادفی بازار
    noise = random.uniform(-100000000, 100000000)
    # قیمت نهایی:
    price = base_price + extras - depreciation + noise
    
    records.append((district, area, rooms, bathrooms, floor, year_built, parking, price))

# درج رکوردها در جدول مربوطه
cursor.executemany('''
INSERT INTO realestate (district, area, rooms, bathrooms, floor, year_built, parking, price)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', records)
conn.commit()
conn.close()

print("پایگاه داده 'realestate.db' با ۱۰۰۰ رکورد واقع‌گرایانه ایجاد شد.")