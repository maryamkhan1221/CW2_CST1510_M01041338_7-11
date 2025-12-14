import pandas as pd
from app.data.db import connect_database


def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Insert a new cybersecurity incident
    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))

    # Save changes
    conn.commit()

    # Get the ID of the new incident
    incident_id = cursor.lastrowid

    # Close the database connection
    conn.close()

    return incident_id


def get_all_incidents():
    # Connect to the database
    conn = connect_database()

    # Load all incidents into a DataFrame
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )

    # Close the database connection
    conn.close()

    return df


def update_incident_status(incident_id, new_status):
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Update the status of a specific incident
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )

    # Save changes
    conn.commit()

    # Close the database connection
    conn.close()


def delete_incident(incident_id):
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Delete an incident by ID
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )

    # Save changes
    conn.commit()

    # Close the database connection
    conn.close()


def get_incidents_by_type():
    # Connect to the database
    conn = connect_database()

    # Count incidents grouped by type
    df = pd.read_sql_query("""
        SELECT incident_type, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY incident_type
        ORDER BY count DESC
    """, conn)

    # Close the database connection
    conn.close()

    return df
