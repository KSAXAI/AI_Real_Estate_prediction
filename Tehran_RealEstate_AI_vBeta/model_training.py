import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# اتصال به پایگاه داده و خواندن داده‌ها
conn = sqlite3.connect('realestate.db')
df = pd.read_sql_query("SELECT * FROM realestate", conn)
conn.close()

# تبدیل ستون 'district' به متغیرهای دامی (بدون drop_first تا همه ۲۲ منطقه حفظ شوند)
df = pd.get_dummies(df, columns=['district'], drop_first=False)

# تعریف ویژگی‌ها و برچسب (قیمت)؛ حذف ستون‌های id و price از ویژگی‌ها
features = [col for col in df.columns if col not in ['id', 'price']]
X = df[features]
y = df['price']

# ذخیره لیست ویژگی‌های مورد انتظار (expected features) برای استفاده در اپلیکیشن
expected_features = X.columns.tolist()

# تقسیم داده‌ها به مجموعه‌های آموزش و تست (۸۰٪ آموزش، ۲۰٪ تست)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# آموزش مدل با استفاده از RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ارزیابی مدل
score = model.score(X_test, y_test)
print(f"امتیاز R^2 مدل در مجموعه تست: {score:.2f}")

# ذخیره مدل آموزش دیده و ویژگی‌های مورد انتظار
joblib.dump(model, 'realestate_model.pkl')
joblib.dump(expected_features, 'expected_features.pkl')
print("مدل و لیست ویژگی‌های مورد انتظار ذخیره شدند.")
