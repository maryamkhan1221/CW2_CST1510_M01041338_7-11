import sqlite3
import os

# Name of the SQLite database file
DATABASE_FILE = "intelligence_platform.db"

def connect_database():
    # Show current working directory (helps with debugging paths)
    print("Working directory:", os.getcwd())
    # Connect to the SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    # Return rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    return conn

def close_database(conn):
    # Safely close the database connection
    if conn:
        conn.close()

def initialize_database():
    # Create the database and tables if they don't exist
    conn = connect_database()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    
    conn.commit()
    close_database(conn)
    print("Database initialized.")

if __name__ == "__main__":
    # Run database setup when this file is executed directly
    initialize_database()
