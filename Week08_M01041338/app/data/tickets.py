import pandas as pd
from app.data.db import connect_database


def insert_ticket(ticket_id, priority, status, category, subject, description, created_date, assigned_to=None):
    # Add a new IT ticket to the database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id, priority, status, category, subject, description, created_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, assigned_to))
    conn.commit()
    conn.close()


def get_all_tickets():
    # Get all IT tickets as a DataFrame
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM it_tickets ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


def update_ticket_status(ticket_id, new_status):
    # Update the status of a ticket
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE it_tickets SET status = ? WHERE ticket_id = ?",
        (new_status, ticket_id)
    )
    conn.commit()
    conn.close()


def delete_ticket(ticket_id):
    # Remove a ticket from the database
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM it_tickets WHERE ticket_id = ?",
        (ticket_id,)
    )
    conn.commit()
    conn.close()
