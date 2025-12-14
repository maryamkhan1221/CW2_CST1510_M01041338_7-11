# Database connection and setup file

import sqlite3
from pathlib import Path

# Path to the SQLite database file
DB_PATH = Path("DATA") / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    # Connect to the SQLite database (creates it if missing)
    # Make sure the DATA folder exists first
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))


def close_database(conn):
    # Safely close the database connection
    if conn:
        conn.close()


def setup_database():
    # Create all required tables for the IT ticket system
    conn = connect_database()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );
    """)

    # Create statuses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT UNIQUE NOT NULL
        );
    """)

    # Insert default statuses if they do not exist
    cursor.execute("SELECT COUNT(*) FROM statuses WHERE status_name = 'Open'")
    if cursor.fetchone()[0] == 0:
        initial_statuses = [
            ('Open',),
            ('In Progress',),
            ('Awaiting User Reply',),
            ('Closed',)
        ]
        cursor.executemany(
            "INSERT INTO statuses (status_name) VALUES (?)",
            initial_statuses
        )

    # Create IT tickets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,

            status_id INTEGER NOT NULL,
            reported_by_user_id INTEGER NOT NULL,
            assigned_agent_id INTEGER,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (status_id) REFERENCES statuses(id),
            FOREIGN KEY (reported_by_user_id) REFERENCES users(id),
            FOREIGN KEY (assigned_agent_id) REFERENCES users(id)
        );
    """)

    # Create ticket updates (comments/logs) table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (ticket_id) REFERENCES it_tickets(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    # Save changes and close connection
    conn.commit()
    conn.close()


def reset_database():
    # Delete all tables (used for testing or development reset)
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ticket_updates")
    cursor.execute("DROP TABLE IF EXISTS it_tickets")
    cursor.execute("DROP TABLE IF EXISTS statuses")
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()
    print(f"Database tables reset successfully in {DB_PATH}.")


if __name__ == "__main__":
    # Run database setup when this file is executed directly
    try:
        setup_database()
        conn = connect_database()
        print(f"Connected to database: {DB_PATH}")
        print("Database schema initialized/verified.")
        close_database(conn)
    except Exception as e:
        print(f"Error: {e}")
