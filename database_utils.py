import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect("bus_details.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Bus_Name TEXT,
            Bus_Type TEXT,
            Departing_Time TEXT,
            Duration TEXT,
            Reaching_Time TEXT,
            Star_Rating TEXT,
            Price TEXT,
            Seat_Availability TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_data_in_db(data):
    conn = sqlite3.connect("bus_details.db")
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO bus_details (Bus_Name, Bus_Type, Departing_Time, Duration, Reaching_Time, Star_Rating, Price, Seat_Availability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def print_summary():
    conn = sqlite3.connect("bus_details.db")
    df = pd.read_sql_query("SELECT * FROM bus_details", conn)
    conn.close()
    
    print("\nSummary of Bus Data:")
    print(f"Total Buses: {len(df)}")
    
if __name__ == "__main__":
    create_database()
    df = pd.read_csv('bus_details.csv')
    store_data_in_db(df.values.tolist())
    print_summary()