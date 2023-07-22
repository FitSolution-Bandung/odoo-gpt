from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

import os
import re
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

from utils.get_credential import get_credentials, is_valid_token
from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

from typing import Optional


from utils.database import init_app, db_sqlalchemy, app
from utils.database import User as User
from utils.database import Message as Message


 



# Fungsi untuk mengirim pesan WhatsApp menggunakan API Wablas
def send_whatsapp_message(phone_number, message):
    url = "https://pati.wablas.com/api/v2/send-message"
    token = os.environ['WABLAS TOKEN']  # Mengambil token dari environment variable

    headers = {"Authorization": token, "Content-Type": "application/json"}

    payload = {"data": [{"phone": phone_number, "message": message}]}


    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    response = requests.post(url,
                             headers=headers,
                             data=json.dumps(payload),
                             verify=False)
    
    result = response.json()

    return result




# Fungsi untuk menangani pesan masuk dari webhook
def handle_incoming_message(data):
     
    incoming_message = ""

    try:
        phone = data.get('phone', None)  # Mengambil nomor telepon pengirim pesan
        incoming_message = data.get('message', None)  # Mengambil isi pesan
        message = ""
        # messageType = data.get('messageType', None)  # Mengambil tipe pesan 

    
        data_str = ""
        for key, value in data.items():
            if value not in [None, ""]:
                data_str += f"{key}: {value}" + "\n"  
        

        
        print(f'Pesan masuk dari {phone}: {incoming_message}')
        print(f"Format sesuai? {re.match(r'^[0-9a-fA-F]{64}$', incoming_message)}")
        
        with app.app_context():
            user = User.query.filter_by(phone_number=phone).first()
            if not user:
                user = User(phone_number=phone, entity_memory=None)
                db_sqlalchemy.session.add(user)
                db_sqlalchemy.session.commit()



        #Check apakah token valid?
        msg = ""
        if is_valid_token(incoming_message) is True:
            credentials = get_credentials(incoming_message)

            if credentials:
                url, username, password, created_at, mobile_phone = credentials
                # Calculate remaining time
                remaining_time = created_at + timedelta(days=5) - datetime.now()
                remaining_hours = remaining_time.total_seconds() // 3600

                message = f"""
                Nama modul: Whatsap.py\n\n
                URL: {url}\nUsername: {username}\nPassword: ***\nMobile Phone: {mobile_phone}\nCreated At: {created_at}\nToken will expire in {remaining_hours} hours"""
                msg = f"\n\ninfo:\n{message}"               
        else:
            message = "Invalid token. Please check your token."
        
        print(f'Respon dikirim ke {phone} : {message}\n')
        
        if phone ==  "628112227980": #Selama masa percobaan, hanya nomor ini yang bisa mengakses
            message = prepare_message(phone, incoming_message) + msg
            send_whatsapp_message(phone, message)  # Mengirim respon ke pengirim pesan

        


        #Tulis record ke database 
        if incoming_message:
            
            msg = Message(user_id=1,
                        user_name=data['sender'],
                        sender=data['sender'],
                        recipient=data['phone'],
                        past=incoming_message,
                        generated=message)
            with app.app_context():
                db_sqlalchemy.session.add(msg)  # Menambahkan objek pesan masuk ke database
                db_sqlalchemy.session.commit()  # Menyimpan perubahan ke database

            #Pesan bila berhasil ditambahkan ke database
            print(f"Message from {phone} added to database")
             

        #tampilkan isi database yang barusan di tambahkan db_sqlalchemy.
             

        with app.app_context():
            message = Message.query.all()
            print(f'All messages: {message}')

 
        
        return jsonify({'status': 'success', 'phone': phone})

    except Exception as e:
        print(f"Error: {e}")
        raise
   


# Fungsi untuk mendapatkan respon dari model chatgpt
def prepare_message(phone, incoming_message):
    session_state = {
    'past': [],
    'generated': []
    }
    
    
    



    # Set the default model and K value
    MODEL = 'gpt-3.5-turbo'
    K = 5
    API_O = os.environ['OPENAI_KEY']


    # Session state storage would be ideal
    if API_O:
        # Create an OpenAI instance
        llm = ChatOpenAI(temperature=0,
                    openai_api_key=API_O,
                    model_name=MODEL,
                    verbose=False)

        # # Create a ConversationEntityMemory object if not already created
        # if 'entity_memory' not in st.session_state:
        #     st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)
        entity_memory = ConversationEntityMemory(llm=llm, k=K)


        print(f'\n\nENTITY_MEMORY_CONVERSATION_TEMPLATE: {ENTITY_MEMORY_CONVERSATION_TEMPLATE}')

        print(f'\n\nConversationEntityMemory: {ConversationEntityMemory}')

        # Create the ConversationChain object with the specified configuration
        Conversation = ConversationChain(llm=llm,
                                       prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                                       memory=entity_memory)
    

    # session_state = []
    # past = session_state["past"]
    # generated = session_state["generated"]

        # if len(past) > 0:
        #     for i in range(0, len(generated)):
        #         with st.chat_message(name="User", avatar="🧑‍💻"):
        #             st.write(past[i])

        #         with st.chat_message(name="Odoo-GPT", avatar="🤖"):
        #                 st.write(generated[i])
     

        # with st.chat_message(name="User", avatar="🧑‍💻"):
        #    st.write(user_input)

        # with st.chat_message(name="Odoo-GPT", avatar="🤖"):
        #     with st.spinner("Memuat Respon ..."):
        output = Conversation.run(input=incoming_message)
        print(f'Output: {output}')

        # Tambahkan pesan ke database
        # message = Message(sender="user", recipient="bot", past=incoming_message, generated=output, user=user)
        # db_sqlalchemy.session.add(message)

        # Perbarui entity_memory
        # user.entity_memory = output  # Sesuaikan ini sesuai dengan kebutuhan Anda


  

     


    return output
    


# def prepare_message(message, phone, model='chatgpt'):
#     try:
#         if model == 'chatgpt':
#           message_response = get_chatgpt_response(phone, message)
#         else:
#           message_response = get_langchain_response(message)

#         # Mengirim pesan balasan menggunakan WhatsApp
#         send_whatsapp_message(phone, message_response)  # Mengirim respon ke pengirim pesan

#         if phone and message:
#             incoming = True
#             msg = Message(phone_number=phone,
#                         message=message,
#                         result="Incoming message",
#                         incoming=incoming)  # Membuat objek pesan masuk
#             db_sqlalchemy.session.add(
#             msg)  # Menambahkan objek pesan masuk ke database
#             db_sqlalchemy.session.commit()  # Menyimpan perubahan ke database
    
#     except Exception as e:
#         print(f"Error: {e}")
#         message_response = "Maaf, terjadi kesalahan pada sistem.\n\n" + str(e)

#         send_whatsapp_message(phone, message_response)
#         incoming = True
#         msg = Message(phone_number=phone,
#                       message=message,
#                       result="Error",
#                       incoming=incoming)  # Membuat objek pesan masuk
        

#         db_sqlalchemy.session.add(msg)  # Menambahkan objek pesan masuk ke database
#         db_sqlalchemy.session.commit()  # Menyimpan perubahan ke database
