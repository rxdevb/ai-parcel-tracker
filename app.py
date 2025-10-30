import time
import psycopg2
import os
import logging
import sys
from typing import Dict, Any, NoReturn

# --- Configuration Constants ---
MAX_RETRIES: int = 5
RETRY_DELAY: int = 3  # Time in seconds to wait between connection attempts
LOG_FORMAT: str = '%(asctime)s - %(levelname)s - %(message)s'

# Configure standard logging to ensure clean, timestamped output.
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def get_db_credentials() -> Dict[str, str]:
    """
    Retrieves database connection parameters from environment variables.

    Returns:
        Dict[str, str]: Dictionary containing host, dbname, user, and password.
    """
    # Use os.environ.get() for secure credential retrieval (with local fallbacks).
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'dbname': os.environ.get('DB_NAME', 'postgres'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'mysecretpassword')
    }


def check_db_connection() -> None:
    """
    Attempts to establish a connection to the PostgreSQL database with multiple retries.

    Exits the process with status 1 if the maximum number of attempts is reached.
    """

    creds: Dict[str, str] = get_db_credentials()

    # The retry loop is vital in containerized environments (Docker/Kubernetes)
    # where the DB may initialize slower than the application.
    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"DB Check: Attempting to connect ({attempt + 1}/{MAX_RETRIES})...")

            # Establish connection using retrieved credentials (**kwargs unpacking).
            conn: Any = psycopg2.connect(**creds)

            logging.info("DB Check: Connection successful.")
            conn.close()
            return  # Successful connection, exit the function.

        except Exception as e:
            logging.error(f"DB Check: Connection failed. Error: {e}")
            if attempt < MAX_RETRIES - 1:
                # Wait before the next attempt.
                logging.warning(f"DB Check: Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                # If all attempts fail, log a critical error and terminate the application.
                logging.critical("DB Check: Maximum connection attempts reached. Terminating application.")
                sys.exit(1)


if __name__ == '__main__':
    # Execute the primary function to verify database connectivity.
    # If this call returns without an exception, the connection is confirmed.
    check_db_connection()

    # In a full application, the main server loop (Flask/Gunicorn) would start here.
    logging.info("DB check passed. Application startup can proceed.")