import sqlite3
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os


# Password encryption
key = os.getenv("ENCRYPT_KEY").encode()
cipher_suite = Fernet(key)


# Fungsi untuk mendapatkan kredensial pengguna berdasarkan token (outputnya : url, username, password, created_at)
def get_credentials(token):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT url, username, password, created_at, mobile_phone FROM users WHERE token = ?", (token,))
    result = c.fetchone()
    conn.close()

    if result:
        url, username, password_encrypted, created_at, mobile_phone = result
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        
        # Check if the token has expired
        if datetime.now() - created_at > timedelta(days=5):
            print('Token has expired')
            return None

        # Decrypt password
        password = cipher_suite.decrypt(password_encrypted).decode()

        return url, username, password, created_at, mobile_phone

    else:
        print(f'No user found with token: {token}')
        return None
    
