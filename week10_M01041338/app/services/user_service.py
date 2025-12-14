import bcrypt
from app.data.db import connect_database

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    try:
        password_bytes = plain_text_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def login_user(username, password):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return False, "Username not found."
        
        if verify_password(password, user['password_hash']):
            return True, user['role']
        else:
            return False, "Invalid password."
    
    except Exception as e:
        return False, f"Login error: {str(e)}"

def register_user(username, password, role="user"):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, f"Username '{username}' already exists."
        
        hashed = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )
        conn.commit()
        conn.close()
        
        return True, f"User '{username}' registered successfully!"
    
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def user_exists(username):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    except Exception:
        return False