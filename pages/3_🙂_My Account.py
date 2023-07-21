import streamlit as st
import utils.login as login 
import utils.logout as logout
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import sqlite3
from utils.token_verification import view_table

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
    


def run():
    
    token = st.session_state['token']

    st.markdown("""
        # You are loged in.
        :information_source: Here is your token.
        Please copy your token and paste it in the field below to verify it. 
    """)
   
            
    # Formulir input token
    with st.form(key='token_form'):
        input_token = st.text_input("Detail Account", value=token)
        submit_token_button = st.form_submit_button(label='Show Credentials')
        
        if submit_token_button and input_token:
            credentials = get_credentials(input_token)
            if credentials:
                url, username, password, created_at = credentials
                
                # Calculate remaining time
                remaining_time = created_at + timedelta(days=5) - datetime.now()
                remaining_hours = remaining_time.total_seconds() // 3600
                
                st.write(f"URL: {url}")
                st.write(f"Username: {username}")
                    
                masked_password = password[:2] + '*' * (len(password) - 2)

                st.write(f"Password: {masked_password}")
                st.write(f"Token will expire in {remaining_hours} hours")
                st.write('---')

                #tampilkan isi table
                with st.expander("Table: 'users'"):
                    view_table('user_data.db', 'users')
            
            else:
                st.error("Invalid token. Please check your token.")

 

#chek token
if st.session_state.get('token') is None:
    st.warning("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
 
    # for param in st.session_state:
    #     st.write(param, st.session_state[param])
    logout.run()