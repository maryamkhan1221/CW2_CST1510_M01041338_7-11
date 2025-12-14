import bcrypt
from pathlib import Path
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table


def register_user(username, password, role='user'):
    # Check if the username is already in the database
    user_exists = get_user_by_username(username)
    if user_exists:
        return False, f"Username '{username}' already exists."

    # Hash the password using bcrypt (salt is generated automatically)
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Save the new user into the database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully!"


def login_user(username, password):
    # Look up the user in the database
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    # Compare the entered password with the stored hash
    stored_hash = user[2]
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    else:
        return False, "Incorrect password."


def migrate_users_from_file(filepath='DATA/users.txt'):
    # Move users from the old text file into the database
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return 0

    # Connect to the database
    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    # Read each line from the file and insert users
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Each line should look like: username,hashed_password
            parts = line.split(',')
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    cursor.execute(
                        "INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, password_hash, 'user')
                    )
                    if cursor.rowcount > 0:
                        migrated_count += 1
                except Exception as e:
                    print(f"Error migrating {username}: {e}")

    # Save changes and close connection
    conn.commit()
    conn.close()
    print(f" Migrated {migrated_count} users")
    return migrated_count
