import streamlit as st
import login 
import logout
import token_verification


def run():
    
    token = st.session_state['token']

    st.markdown("""
        # You are loged in.
        :information_source: Here is your token.
        Please copy your token and paste it in the field below to verify it. 
    """)
    st.code(f"""{token}""", language='text')
    
            

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

           


#chek token
if st.session_state.get('token') is None:
    st.warning("You are not logged in!")
 
    login.run()

else:

    

    # Ambil kredensial (ini hanya contoh, dalam prakteknya jangan tunjukkan password secara langsung)
    username = st.session_state.get('username', 'N/A')
    password = st.session_state.get('password', 'N/A')
    token = st.session_state['token']

    for param in st.session_state:
        st.write(param, st.session_state[param])



    st.markdown(f"""
    ## Account Details

    
    **Username**: {username}

    **Password**: {'*' * len(password)}

    **Token**: ```{token}```


    """)




    st.markdown("""
    ## Account Settings

    If you want to change your account settings, please contact our support team.
    """)

    #Bagian dari ....
    logout.run()