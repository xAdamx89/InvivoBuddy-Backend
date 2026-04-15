# Używamy lekkiej wersji Pythona
FROM python:3.12-slim

# Ustawiamy folder roboczy wewnątrz kontenera
WORKDIR /app

# Instalujemy zależności systemowe potrzebne dla psycopg2 lub asyncpg
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Kopiujemy plik z wymaganiami
COPY requirements.txt .

# Instalujemy biblioteki Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu aplikacji
COPY . .

# Komenda uruchamiająca serwer
# Ważne: host 0.0.0.0 pozwala na ruch z zewnątrz kontenera
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
