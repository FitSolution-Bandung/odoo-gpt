import streamlit as st
import utils.login as login 
import utils.logout as logout
from utils.send_email import send_email
from utils.whatsapp import send_whatsapp_message
 
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
    with st.expander("**Berikut adalah Credential Odoo-GPT Anda:**", expanded=True):
                
        credentials = get_credentials(input_token)
        if credentials:

            url = credentials['url']
            db = credentials['db']
            username = credentials['username']
            password = credentials['password']
            created_at = credentials['created_at']
            phone_number = credentials['phone_number']
            
            print(f'\n\ncredentials: {credentials}\n\n')
            print(f'\n\nurl: {url}\n\n')
            print(f'\n\ncreated at: {created_at}\n\n')
            
            # Calculate remaining time
            remaining_time = created_at + timedelta(days=5) - datetime.now()
            remaining_hours = remaining_time.total_seconds() // 3600
              
            masked_password = password[:2] + '*' * (len(password) - 2)

            st.code(token)
            credentials_text = (
                f"URL: {url}\n\n"
                f"Database: {db}\n\n"
                f"Username: {username}\n\n"
                f"Password: {masked_password}\n\n"
                f"Work Mobile: {phone_number}\n\n"
                f"Token will expire in {remaining_hours} hours"
                
            )
            st.write(credentials_text)
            st.write('---')
            

            
            #Kirimkan Credential ke Email
            if st.button("Send Credential to Email"):
                credentials_html = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                background-color: #f7f9fc;
                                padding: 40px;
                            }}
                            .credentials-box {{
                                background-color: #ffffff;
                                border: 1px solid #e0e0e0;
                                padding: 30px;
                                border-radius: 10px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
                                max-width: 500px;
                                margin: auto;
                            }}
                            .credentials-label {{
                                display: block;
                                color: #555555;
                                font-weight: bold;
                                margin-bottom: 10px;
                            }}
                            .token-code {{
                                display: inline-block;
                                background-color: #f4f4f4;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-family: 'Courier New', Courier, monospace;
                                border: 1px solid #e0e0e0;
                            }}
                            h2 {{
                                color: #333;
                                border-bottom: 2px solid #4CAF50;
                                padding-bottom: 10px;
                                margin-bottom: 20px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="credentials-box">
                            <h2>Credential Odoo-GPT Anda:</h2>
                            <span class="credentials-label">Token: <span class="token-code">{token}</span></span>
                            <span class="credentials-label">URL: {url}</span>
                            <span class="credentials-label">Database: {db}</span>
                            <span class="credentials-label">Username: {username}</span>
                            <span class="credentials-label">Password: {masked_password}</span>
                            <span class="credentials-label">Work Mobile: {phone_number}</span>
                            <span class="credentials-label">Token Expiry: {remaining_hours} hours</span>
                        </div>
                    </body>
                </html>
                """


                send_email(subject="Your Odoo-GPT Credentials", message=credentials_html, to_email=username)

            #Kirimkan Credential ke WhatsApp
            if st.button("Send Credential to WhatsApp"):

                # Format teks untuk WhatsApp
                bold = lambda text: f"*{text}*"
                italic = lambda text: f"_{text}_"
                code = lambda text: f"```{text}```"
                credentials_whatsapp = (
                    f"{bold('Credential Odoo-GPT Anda:')}\n\n"
                    f"{bold('Token:')} {code(token)}\n\n"
                    f"{bold('URL:')} {url}\n"
                    f"{bold('Database:')} {db}\n"
                    f"{bold('Username:')} {username}\n"
                    f"{bold('Password:')} {masked_password}\n"
                    f"{bold('Work Mobile:')} {phone_number}\n"
                    f"{bold('Token Expiry:')} {remaining_hours} hours"
                )
                # message = credentials_text.replace('\n\n', '\n')
                send_whatsapp_message(phone_number=phone_number, message=credentials_whatsapp)




#chek token
if st.session_state.get('token') is None:
    st.error("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()