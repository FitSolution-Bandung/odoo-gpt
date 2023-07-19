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




def run():
    
    st.markdown("""
        # You are loged in.
                    
        :information_source: Your token: `{}`
        Please click the button below to go to the Token Verification Page.
        """.format(st.session_state['token']), unsafe_allow_html=True)
        

    # Formulir input token
    with st.form(key='token_form'):
        input_token = st.text_input("Enter your token")
        submit_token_button = st.form_submit_button(label='Submit Token')
        
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

           

    # Tombol logout
    logout_button = st.button('Logout')
    if logout_button:
        st.session_state['token'] = None
        st.session_state['logged_in'] = False
        st.experimental_rerun() # Refresh halaman

