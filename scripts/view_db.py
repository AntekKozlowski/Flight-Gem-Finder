import sqlite3
import pandas as pd


def view_data():
    conn = sqlite3.connect("../flights_history.db")

    print("--- RAW SQL DATA ---")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_history")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


if __name__ == "__main__":
    view_data()