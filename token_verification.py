import sqlite3
from cryptography.fernet import Fernet
import streamlit as st  
from datetime import datetime, timedelta

# Anda harus mengubah ini dengan kunci yang Anda gunakan untuk enkripsi password
key = b'4Gpyw4r57coCTSULSqGcq2ywpECnRK3fkAHcJvWqc08='

cipher_suite = Fernet(key)

def get_credentials(token):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT url, username, password, created_at FROM users WHERE token = ?", (token,))
    result = c.fetchone()
    conn.close()

    if result:
        url, username, password_encrypted, created_at = result
        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        
        # Check if the token has expired
        if datetime.now() - created_at > timedelta(days=5):
            print('Token has expired')
            return None

        # Decrypt password
        password = cipher_suite.decrypt(password_encrypted).decode()

        return url, username, password, created_at

    else:
        print(f'No user found with token: {token}')
        return None
    
    
#Lihat isi  database di sqlite
def view_tables(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        st.write(f"Table name: {table[0]}")
        
    con.close()

#Lihat isi table
def view_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        st.write(row)
   
    con.close()



#Hapus semua isi table
def clear_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    cursor.execute(f"DELETE FROM {table_name};")
    con.commit()
    
    print("All rows deleted from table 'user'")
    
    con.close()







    #Tombol Eksekusi Chat.py
    # chat_button = st.button('Go to Chat')
    # if chat_button:
    #     import pages.chat as chat
    #     chat.run()


