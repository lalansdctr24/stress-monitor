# Gunakan image Python yang ringan
FROM python:3.11-slim

# Set direktori kerja
WORKDIR /app

# Salin file aplikasi ke dalam container
COPY app/ ./app/
COPY requirements.txt .

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan aplikasi Flask
CMD ["python", "app/main.py"]
