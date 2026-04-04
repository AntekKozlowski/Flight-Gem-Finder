import sqlite3
from datetime import datetime

DB_NAME = "flights_history.db"


def setup_database():
    """Initializes SQLite database with search history and API cache tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT NOT NULL,
            is_gem BOOLEAN NOT NULL,
            score INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            origin TEXT,
            destination TEXT,
            outbound_date TEXT,
            return_date TEXT,
            price REAL,
            duration TEXT,
            stops INTEGER,
            carrier TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            layovers TEXT
        )
    ''')

    conn.commit()
    conn.close()


def save_flight_record(origin: str, dest: str, price: float, is_gem: bool, score: int):
    """Saves final AI analysis results to the historical database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO search_history (timestamp, origin, destination, price, currency, is_gem, score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (now, origin, dest, price, "PLN", is_gem, score))

    conn.commit()
    conn.close()


def get_cached_flight(origin: str, destination: str, outbound_date: str, return_date: str) -> dict | None:
    """Retrieves flight data from the cache if queried within the last 24 hours."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT price, duration, stops, carrier, departure_time, arrival_time, layovers FROM api_cache 
        WHERE origin = ? AND destination = ? AND outbound_date = ? AND IFNULL(return_date, '') = ?
        AND timestamp >= datetime('now', '-1 day')
        ORDER BY timestamp DESC LIMIT 1
    ''', (origin, destination, outbound_date, return_date or ''))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "price": row[0],
            "currency": "PLN",
            "duration": row[1],
            "stops": row[2],
            "carrier": row[3],
            "departure_time": row[4],
            "arrival_time": row[5],
            "layovers": row[6]
        }
    return None


def save_cached_flight(origin: str, destination: str, outbound_date: str, return_date: str, flight: dict):
    """Saves a fresh API response to the cache table to minimize external API calls."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO api_cache (origin, destination, outbound_date, return_date, price, duration, stops, carrier, departure_time, arrival_time, layovers)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (origin, destination, outbound_date, return_date or '', flight['price'], flight['duration'], flight['stops'],
          flight['carrier'], flight['departure_time'], flight['arrival_time'], flight['layovers']))

    conn.commit()
    conn.close()