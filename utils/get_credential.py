import sqlite3
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import re
from dotenv import load_dotenv  

# Password encryption
load_dotenv('.credentials\.env')
key = os.getenv("ENCRYPT_KEY").encode()
cipher_suite = Fernet(key)

# Fungsi untuk mendapatkan kredensial pengguna berdasarkan token (outputnya : url, username, password, created_at)
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os
import re
from utils.database import User, db_sqlalchemy, app


# Password encryption
load_dotenv('/.credentials/.env')
key = os.getenv("ENCRYPT_KEY").encode()
cipher_suite = Fernet(key)

Base = declarative_base()



def get_credentials(token):
    
    with app.app_context():
        session = db_sqlalchemy.session
        user = session.query(User).filter_by(token=token).first()

        # db_sqlalchemy.session.delete(user)
        # db_sqlalchemy.session.commit()

    if user:
        url = user.url
        db = user.db
        username = user.username
        password_encrypted = user.password
        phone_number = user.phone_number
        created_at = user.created_at


        # Check if the token has expired
        if datetime.now() - created_at > timedelta(days=5):
            print('Token has expired')
            return None

        # Decrypt password
        # password = cipher_suite.decrypt(password_encrypted.encode()).decode()
        password = cipher_suite.decrypt(password_encrypted).decode()



        data_dict = {
            'url': url,
            'db': db,
            'username': username,
            'password': password,
            'created_at': created_at,
            'phone_number': phone_number

        }



        print(f'User found with token: {token}')
        print(f'User data: {data_dict}')

        return data_dict

    else:
        print(f'NO user found with token: {token}')
        return None

    



def is_valid_token(token):
    if len(token) != 64: 
        return False
    if not re.match(r'^[0-9a-fA-F]*$', token): 
        return False
    return True

