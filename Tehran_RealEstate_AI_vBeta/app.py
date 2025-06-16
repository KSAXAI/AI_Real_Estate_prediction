from flask import Flask, request, render_template, url_for
import pandas as pd
import joblib

app = Flask(__name__)

# بارگذاری مدل آموزش دیده و لیست ویژگی‌های مورد انتظار
model = joblib.load('realestate_model.pkl')
expected_features = joblib.load('expected_features.pkl')

# تعریف 22 منطقه تهران
available_districts = [f"منطقه_{i}" for i in range(1, 23)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # دریافت داده‌های فرم
            district = request.form.get('district')
            area = float(request.form.get('area'))
            rooms = int(request.form.get('rooms'))
            bathrooms = int(request.form.get('bathrooms'))
            floor = int(request.form.get('floor'))
            year_built = int(request.form.get('year_built'))
            parking = int(request.form.get('parking'))
            
            # ساخت دیکشنری ورودی با ویژگی‌های اصلی
            data = {
                'area': area,
                'rooms': rooms,
                'bathrooms': bathrooms,
                'floor': floor,
                'year_built': year_built,
                'parking': parking
            }
            
            # برای هر ستون dummy (دسته‌ای) انتظار داریم که در ورودی باشد، مقدار پیش‌فرض صفر قرار می‌دهیم
            for col in expected_features:
                if col.startswith('district_'):
                    data[col] = 0
            
            # ست کردن مقدار 1 برای ستون دامی مربوط به منطقه انتخاب شده
            dummy_col = f"district_{district}"
            if dummy_col in expected_features:
                data[dummy_col] = 1
            
            # ایجاد DataFrame با ترتیب دقیق همان لیست ویژگی‌های مورد انتظار
            input_df = pd.DataFrame([data], columns=expected_features)
            
            # پیش‌بینی قیمت
            prediction = model.predict(input_df)[0]
            return render_template('result.html', prediction=round(prediction, 2))
        except Exception as e:
            return f"خطا: {str(e)}"
    return render_template('index.html', districts=available_districts)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, url_for
import pandas as pd
import joblib

app = Flask(__name__)

# بارگذاری مدل آموزش دیده و لیست ویژگی‌های مورد انتظار
model = joblib.load('realestate_model.pkl')
expected_features = joblib.load('expected_features.pkl')

# تعریف 22 منطقه تهران
available_districts = [f"منطقه_{i}" for i in range(1, 23)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # دریافت داده‌های فرم
            district = request.form.get('district')
            area = float(request.form.get('area'))
            rooms = int(request.form.get('rooms'))
            bathrooms = int(request.form.get('bathrooms'))
            floor = int(request.form.get('floor'))
            year_built = int(request.form.get('year_built'))
            parking = int(request.form.get('parking'))
            
            # ساخت دیکشنری ورودی با ویژگی‌های اصلی
            data = {
                'area': area,
                'rooms': rooms,
                'bathrooms': bathrooms,
                'floor': floor,
                'year_built': year_built,
                'parking': parking
            }
            
            # برای هر ستون dummy (دسته‌ای) انتظار داریم که در ورودی باشد، مقدار پیش‌فرض صفر قرار می‌دهیم
            for col in expected_features:
                if col.startswith('district_'):
                    data[col] = 0
            
            # ست کردن مقدار 1 برای ستون دامی مربوط به منطقه انتخاب شده
            dummy_col = f"district_{district}"
            if dummy_col in expected_features:
                data[dummy_col] = 1
            
            # ایجاد DataFrame با ترتیب دقیق همان لیست ویژگی‌های مورد انتظار
            input_df = pd.DataFrame([data], columns=expected_features)
            
            # پیش‌بینی قیمت
            prediction = model.predict(input_df)[0]
            return render_template('result.html', prediction=round(prediction, 2))
        except Exception as e:
            return f"خطا: {str(e)}"
    return render_template('index.html', districts=available_districts)

if __name__ == '__main__':
    app.run(debug=True)
