import streamlit as st
import utils.login as login 
import utils.logout as logout
 
from datetime import datetime, timedelta

from utils.table_operation import view_table
import os
from  utils.get_credential import get_credentials




def run():

    if 'token' not in st.session_state:
        st.session_state['token'] = ""
        
    token = st.session_state['token']

    st.markdown("""
        # You are loged in.
                   
        :information_source: Here is your token.
        Please copy your token and paste it in the field below to verify it. 
    """)
   
                
    # Formulir input token
    with st.form(key='token_form'):
        input_token = token
        st.code(token)
        submit_token_button = st.form_submit_button(label='Show Credentials')
            
    if submit_token_button and input_token:
        credentials = get_credentials(input_token)
        if credentials:
            url, username, password, created_at, phone_number = credentials
            
            # Calculate remaining time
            remaining_time = created_at + timedelta(days=5) - datetime.now()
            remaining_hours = remaining_time.total_seconds() // 3600
            
            st.write('Detail Account:')
            st.write(f"URL: {url}")
            st.write(f"Username: {username}")
            st.write(f"Work Mobile: {phone_number}")
                
            masked_password = password[:2] + '*' * (len(password) - 2)

            st.write(f"Password: {masked_password}")
            st.write(f"Token will expire in {remaining_hours} hours")
            st.write('---')

            #tampilkan isi table
            # with st.expander("Table: 'users'"):
            #     view_table('user_data.db', 'users')
        
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
    # logout.run()