import pandas as pd
from app.data.db import connect_database


# CREATE
def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents
        (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


# READ (all)
def get_all_incidents():
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df


# READ (single)  ← ADDED
def get_incident_by_id(incident_id):
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(incident_id,)
    )
    conn.close()
    return df


# UPDATE (status only – kept as-is)
def update_incident_status(incident_id, new_status):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    conn.close()


# UPDATE (full record)  ← ADDED
def update_incident(
    incident_id,
    date,
    incident_type,
    severity,
    status,
    description,
    reported_by
):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cyber_incidents
        SET date = ?, incident_type = ?, severity = ?, status = ?, description = ?, reported_by = ?
        WHERE id = ?
    """, (date, incident_type, severity, status, description, reported_by, incident_id))
    conn.commit()
    conn.close()


# DELETE
def delete_incident(incident_id):
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM cyber_incidents WHERE id = ?",
        (incident_id,)
    )
    conn.commit()
    conn.close()


# READ (analytics – kept)
def get_incidents_by_type():
    conn = connect_database()
    df = pd.read_sql_query("""
        SELECT incident_type, COUNT(*) as count
        FROM cyber_incidents
        GROUP BY incident_type
        ORDER BY count DESC
    """, conn)
    conn.close()
    return df
