# Dockerfile للـ Backend
FROM python:3.11-slim

WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات Backend
COPY . .

# إنشاء مجلدات للبيانات
RUN mkdir -p /app/logs

# Port
EXPOSE 8000

# تشغيل السيرفر
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
