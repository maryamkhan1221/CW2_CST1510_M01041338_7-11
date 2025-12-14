import bcrypt
import os

# File where usernames + hashed passwords + roles are stored
USER_FILE = "users.txt"

def hash_password(plain_text_password):
    # Hash a normal password using bcrypt (salt is generated automatically)
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    # Check if a password matches the stored bcrypt hash
    try:
        password_bytes = plain_text_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

# --- File helper functions ---

def _load_users():
    # Read users.txt and return users in a dictionary
    # File format: username,password_hash,role
    users = {}
    if not os.path.exists(USER_FILE):
        return users

    with open(USER_FILE, 'r') as f:
        for line in f:
            try:
                username, password_hash, role = line.strip().split(',', 2)
                users[username] = {'password_hash': password_hash, 'role': role}
            except ValueError:
                # Skip any broken lines
                continue
    return users

def _save_users(users):
    # Write the full users dictionary back into users.txt
    with open(USER_FILE, 'w') as f:
        for username, data in users.items():
            line = f"{username},{data['password_hash']},{data['role']}\n"
            f.write(line)

# --- Main functions ---

def login_user(username, password):
    # Login: check username exists + password is correct
    try:
        users = _load_users()
        user_data = users.get(username)

        if not user_data:
            return False, "Username not found."

        if verify_password(password, user_data['password_hash']):
            return True, user_data['role']
        else:
            return False, "Invalid password."

    except Exception as e:
        return False, f"Login error: {str(e)}"

def register_user(username, password, role="user"):
    # Register: add a new user if the username is not taken
    try:
        users = _load_users()

        if username in users:
            return False, f"Username '{username}' already exists."

        hashed = hash_password(password)

        users[username] = {
            'password_hash': hashed,
            'role': role
        }

        _save_users(users)
        return True, f"User '{username}' registered successfully!"

    except Exception as e:
        return False, f"Registration error: {str(e)}"

def user_exists(username):
    # Quick check if a username exists in users.txt
    try:
        users = _load_users()
        return username in users
    except Exception:
        return False

# Test code (runs only if you execute this file directly)
if __name__ == '__main__':
    # Register a user
    success, message = register_user("testuser", "securepassword123", "admin")
    print(f"Registration: {success}, {message}")

    # Check user exists
    exists = user_exists("testuser")
    print(f"User exists: {exists}")

    # Login with correct password
    logged_in, result = login_user("testuser", "securepassword123")
    print(f"Login success: {logged_in}, Role/Message: {result}")

    # Login with wrong password
    logged_in_fail, result_fail = login_user("testuser", "wrongpassword")
    print(f"Login failure: {logged_in_fail}, Message: {result_fail}")
