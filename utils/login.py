import streamlit as st
import xmlrpc.client
import hashlib
from cryptography.fernet import Fernet

from datetime import datetime
from urllib.parse import urlparse
from socket import gaierror

from flask_sqlalchemy import SQLAlchemy

from utils.database import User, db_sqlalchemy, app


key = b'4Gpyw4r57coCTSULSqGcq2ywpECnRK3fkAHcJvWqc08='
cipher_suite = Fernet(key)


def verify_user(url, db, username, password):
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})

    if uid:
        # create an object for the 'models' service
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

        # Search for the hr.employee record that has the same email as the User
        employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[['work_email', '=', username]]])

        # If an employee is found, read the mobile_phone field
        if employee_ids:
            employee = models.execute_kw(db, uid, password, 'hr.employee', 'read', [employee_ids, ['mobile_phone','nick_name']])
            mobile_phone = employee[0]['mobile_phone'] if employee[0]['mobile_phone'] else None
            nick_name = employee[0]['nick_name'] if employee[0]['nick_name'] else None
            return uid, mobile_phone, nick_name
        else:
            return uid, None
    else:
        return None


def store_credentials(url, db, username, password):
    token = hashlib.sha256((url + db + username + password).encode()).hexdigest()

    password_encrypted = cipher_suite.encrypt(password.encode())

    #get mobile phone
    mobile_phone = verify_user(url, db, username, password)[1]
    nick_name = verify_user(url, db, username, password)[2]
    
    print(f'Modul Login :\n\n Nick Name: {nick_name}\nMobile phone: {mobile_phone}')

    # Simpan waktu saat ini dalam format string
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with app.app_context():
        # Cari User dengan url, db, dan username yang sama
        user_query = User.query.filter_by(url=url, db=db, username=username).first()
        print(f'User: {user_query}')


       
        ##Proses penyimpanan data ke database

        # Cari User dengan url, db, dan username yang sama
        # user_query = User.query.filter_by(url=url, db=db, username=username).first()
        # print(f'User: {user_query}')
        if user_query is None:
            # Jika User belum ada, buat User baru
            print(f'url: {url}\ndb: {db}\nusername: {username}\npassword: {password_encrypted}\ntoken: {token}\ncreated_at: {now}\nmobile_phone: {mobile_phone}\nnick_name: {nick_name} ')

            user_query = User(url=url, db=db, username=username, password=password_encrypted, token=token, phone_number=mobile_phone, nick_name=nick_name)
            db_sqlalchemy.session.add(user_query)
            db_sqlalchemy.session.commit()
        else:
            # Jika User sudah ada, update User
            user_query.password = password_encrypted
            user_query.token = token
            user_query.phone_number = mobile_phone
            user_query.nick_name = nick_name
            print(f'Mau di update \n\nurl: {url}\ndb: {db}\nusername: {username}\npassword: {password_encrypted}\ntoken: {token}\ncreated_at: {now}\phone_number: {mobile_phone}\nnick_name: {nick_name} ')

            db_sqlalchemy.session.commit()

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

                    print(f'User ID: {str(user_id)}')

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