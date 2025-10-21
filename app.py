# app.py (zmieniona sekcja)
import time # Dodaj import time
import psycopg2

MAX_RETRIES = 5
RETRY_DELAY = 3 # seconds

# ... (pozostały kod i zmienne środowiskowe) ...

for attempt in range(MAX_RETRIES):
    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        print("Successfully connected to the PostgreSQL database!")
        conn.close()
        break # Jeśli się połączyło, wychodzimy z pętli
    except Exception as e:
        print(f"Failed to connect to the database (Attempt {attempt+1}/{MAX_RETRIES}): {e}")
        if attempt < MAX_RETRIES - 1:
            print(f"Waiting {RETRY_DELAY} seconds before retrying...")
            time.sleep(RETRY_DELAY)
        else:
            print("Maximum connection attempts reached. Exiting application.")
            exit(1) # Zmusza aplikację do wyjścia z błędem po niepowodzeniu