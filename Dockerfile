# Użycie oficjalnego obrazu Pythona
FROM python:3.9-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj plik z zależnościami i zainstaluj je
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj plik z kodem Twojej aplikacji
COPY app.py .

# Uruchom aplikację Pythona
CMD ["python", "app.py"]