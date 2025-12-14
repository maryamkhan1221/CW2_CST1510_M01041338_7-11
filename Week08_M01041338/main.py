from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import insert_incident, get_all_incidents
import pandas as pd


def load_csv_data(conn):
    # Load CSV files into the database using the same connection

    try:
        users_df = pd.read_csv('DATA/users.csv')
        users_df.to_sql('users', conn, if_exists='replace', index=False)
        print(f" Loaded {len(users_df)} users")
    except Exception as e:
        print(f"  Users: {e}")

    try:
        incidents_df = pd.read_csv('DATA/cyber_incidents.csv')
        incidents_df.to_sql('cyber_incidents', conn, if_exists='replace', index=False)
        print(f" Loaded {len(incidents_df)} cyber incidents")
    except Exception as e:
        print(f"  Incidents: {e}")

    try:
        tickets_df = pd.read_csv('DATA/it_tickets.csv')
        tickets_df.to_sql('it_tickets', conn, if_exists='replace', index=False)
        print(f" Loaded {len(tickets_df)} IT tickets")
    except Exception as e:
        print(f"  Tickets: {e}")

    try:
        datasets_df = pd.read_csv('DATA/datasets_metadata.csv')
        datasets_df.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
        print(f" Loaded {len(datasets_df)} datasets")
    except Exception as e:
        print(f"  Datasets: {e}")


def test_authentication():
    # Quick test: register a user and then try logging in
    success, msg = register_user("bob", "SecurePass123!", "analyst")
    print(f"Register: {msg}")

    success, msg = login_user("bob", "SecurePass123!")
    print(f"Login: {msg}")


def test_crud():
    # Quick test: create one incident record
    incident_id = insert_incident(
        date="2024-11-05",
        incident_type="Phishing",
        severity="High",
        status="Open",
        description="Suspicious email detected",
        reported_by="bob"
    )
    print(f"Created incident #{incident_id}")


def query_data():
    # Pull data from the database and print a small preview
    df = get_all_incidents()
    print(f"Total incidents: {len(df)}")
    print("\nFirst 5 incidents:")
    print(df.head(5))


def main():
    # Run the full demo step-by-step
    print("=" * 60)
    print("Week 8: Database Demo")
    print("=" * 60)

    print("\n[1/6] Setting up database...")
    conn = connect_database()
    create_all_tables(conn)

    print("\n[2/6] Loading CSV data...")
    load_csv_data(conn)

    print("\n[3/6] Testing authentication...")
    test_authentication()

    print("\n[4/6] Testing CRUD operations...")
    test_crud()

    print("\n[5/6] Querying data...")
    query_data()

    # Close database connection at the end
    conn.close()

    print("\n" + "=" * 60)
    print(" Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    # Only run main() if this file is executed directly
    main()
