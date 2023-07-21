import streamlit as st
import xmlrpc.client
import sqlite3
import hashlib
from cryptography.fernet import Fernet
import utils.token_verification as token_verification
from datetime import datetime, timedelta
from urllib.parse import urlparse
from socket import gaierror
 


key = b'4Gpyw4r57coCTSULSqGcq2ywpECnRK3fkAHcJvWqc08='
cipher_suite = Fernet(key)


def verify_user(url, db, username, password):
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})

    if uid:
        return uid
    else:
        return None


def drop_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    con.commit()
    
    print(f"Table '{table_name}' has been dropped.")
        
    con.close()



def store_credentials(url, db, username, password):
    token = hashlib.sha256((url + db + username + password).encode()).hexdigest()

    password_encrypted = cipher_suite.encrypt(password.encode())
    
    # Simpan waktu saat ini dalam format string
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()

    # Cek apakah record dengan url, db, dan username yang sama sudah ada
    c.execute("SELECT * FROM users WHERE url = ? AND db = ? AND username = ?", (url, db, username))
    record = c.fetchone()

    if record is None:
        # Jika record belum ada, buat record baru
        c.execute("INSERT INTO users (url, db, username, password, token, created_at) VALUES (?, ?, ?, ?, ?, ?)", 
                  (url, db, username, password_encrypted, token, now))
    else:
        # Jika record sudah ada, update record
        c.execute("UPDATE users SET password = ?, token = ?, created_at = ? WHERE url = ? AND db = ? AND username = ?", 
                  (password_encrypted, token, now, url, db, username))

    conn.commit()
    conn.close()

    return token


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

 
 
 

def run():

     
    if 'token' not in st.session_state or not st.session_state['token']:

        st.markdown("""
                    # Login to Odoo
                    """)

        with st.form(key='login_form'):
            url = st.text_input("Odoo URL", value='https://erp.fujicon-japan.com')
            db = st.text_input("Database", value='erp')
            username = st.text_input("Username", value='andhi@fujicon-japan.com')
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label='Login')

            
            if submit_button and is_valid_url(url) and db and username and password:
                try:
                    user_id = verify_user(url, db, username, password)
                    if user_id:
                        st.success("Login successful!")
                        token = store_credentials(url, db, username, password)
                        st.session_state['token'] = token
                        st.write("Your token: ", token)
                        st.session_state['logged_in'] = True
                        st.experimental_rerun()
                        
                    
                
                    else:
                        st.error("Login failed. Please check your credentials.")
                        st.session_state['token'] = None

                except gaierror:
                    st.error("Failed to connect to the specified URL. Please check the URL and try again.")


    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        token_verification.run()


        
      