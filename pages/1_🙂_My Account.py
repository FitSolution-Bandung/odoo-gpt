import streamlit as st
import utils.login as login 
import utils.logout as logout
 
from datetime import datetime, timedelta

from utils.table_operation import view_table
import os
from utils.get_credential import get_credentials
from utils import sidebar as sidebar




def run():

    sidebar.run()



    if 'token' not in st.session_state:
        st.session_state['token'] = ""
        
    token = st.session_state['token']

    st.markdown("""
        # You are loged in.                 
        **💡 Here is your token. You can copy the token from the code box below.**\n
        Send this token to the administrator's WhatsApp number to obtain the credentials to log into the Odoo system.
    """)
                   
    # Formulir input token
    input_token = token
    st.code(token)
     
    with st.expander("Show Credential Details"):
                
        credentials = get_credentials(input_token)
        if credentials:

            url = credentials['url']
            db = credentials['db']
            username = credentials['username']
            password = credentials['password']
            created_at = credentials['created_at']
            phone_number = credentials['phone_number']
            
            # url, db, username, password, created_at, phone_number = credentials

            print(f'\n\ncredentials: {credentials}\n\n')
            print(f'\n\nurl: {url}\n\n')
            print(f'\n\ncreated at: {created_at}\n\n')
            
            # Calculate remaining time
            remaining_time = created_at + timedelta(days=5) - datetime.now()
            remaining_hours = remaining_time.total_seconds() // 3600
            
            st.write(f"URL: {url}")
            st.write(f"Username: {username}")
            st.write(f"Work Mobile: {phone_number}")
                
            masked_password = password[:2] + '*' * (len(password) - 2)

            st.write(f"Password: {masked_password}")
            st.write(f"Token will expire in {remaining_hours} hours")

           
    

   


#chek token
if st.session_state.get('token') is None:
    st.error("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
 
    # for param in st.session_state:
    #     st.write(param, st.session_state[param])
    # logout.run()