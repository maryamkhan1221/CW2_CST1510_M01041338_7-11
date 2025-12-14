import pandas as pd
from app.data.db import connect_database


def insert_dataset(dataset_name, category, source, last_updated, record_count, file_size_mb):
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Insert a new dataset record
    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated, record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))

    # Save changes
    conn.commit()

    # Get the ID of the inserted dataset
    dataset_id = cursor.lastrowid

    # Close the database connection
    conn.close()

    return dataset_id


def get_all_datasets():
    # Connect to the database
    conn = connect_database()

    # Read all datasets into a DataFrame
    df = pd.read_sql_query(
        "SELECT * FROM datasets_metadata ORDER BY id DESC",
        conn
    )

    # Close the database connection
    conn.close()

    return df


def delete_dataset(dataset_id):
    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()

    # Delete a dataset by its ID
    cursor.execute(
        "DELETE FROM datasets_metadata WHERE id = ?",
        (dataset_id,)
    )

    # Save changes
    conn.commit()

    # Close the database connection
    conn.close()
