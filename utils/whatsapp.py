from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

import os
import re
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from utils.get_credential import get_credentials, is_valid_token

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE

# from langchain.memory import ConversationBufferWindowMemory
# from langchain.chains import ConversationChain

from typing import Optional


from utils.database import init_app, db_sqlalchemy, app
from utils.database import User as User
from utils.database import Message as Message
from utils.database import write_chat_to_db

from pprint import pprint


 



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
    credentials = None
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
        
        

        #chek apakah nomor telepon sudah ada di database
        with app.app_context():
            user = User.query.filter_by(phone_number=phone).first()

            if user:
                msg = ""
                #lakukan pengecekan apabila format pesan masuk sesuai dengan format token
                if re.match(r'^[0-9a-fA-F]{64}$', incoming_message):
                    #Check apakah token valid ketika pesan masuk sama dengan token yang ada di database
                    
                    credentials = get_credentials(incoming_message)
                    print(f'Credentials: {credentials}')    
                    print(f"Format sesuai? {re.match(r'^[0-9a-fA-F]{64}$', incoming_message)}")

                    if credentials is not None:
                        url, username, password, created_at, mobile_phone = credentials
                        # Calculate remaining time
                        remaining_time = created_at + timedelta(days=5) - datetime.now()
                        remaining_hours = remaining_time.total_seconds() // 3600

                        msg = f"""Terimakasih Token anda sudah diverifikasi.\n\nURL: {url}\nUsername: {username}\nPassword: ***\nMobile Phone: {mobile_phone}\nCreated At: {created_at}\nToken will expire in {remaining_hours} hours"""
                        msg += "\n\nApakah ada yang bisa saya bantu?"            

                    else:
                        msg = "Invalid token. Please check your token."
           

                    message = msg
                    send_whatsapp_message(phone, message)  # Mengirim respon ke pengirim pesan
                    print(f'Pesan hasil pengecekan Token: {msg}')
                    exit()


                
            
            
            else:
                
                user = User(phone_number=phone)
                db_sqlalchemy.session.add(user)
                db_sqlalchemy.session.commit()

       
        # if phone ==  "628112227980": #Selama masa percobaan, hanya nomor ini yang bisa mengakses
        if phone and incoming_message:    

            message = prepare_message(phone, incoming_message)
            
            send_whatsapp_message(phone, message)  # Mengirim respon ke pengirim pesan

        





        #Tulis record ke database 
        if incoming_message:
            sender = "62811XXXX"
            write_chat_to_db(phone, incoming_message, sender, message)
            #Pesan bila berhasil ditambahkan ke database
            print(f"Message from {phone} added to database")
             
              

        # with app.app_context():
        #     message = Message.query.all()
        #     print(f'All messages: {message}')

 
        
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
    K = 10
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

        #chek apakah nomor telepon sudah ada di database
 
        with app.app_context():
            user_query = User.query.filter_by(phone_number=phone).first()
            buf_memory = user_query.entity_memory




        if buf_memory is None:
            memory = ConversationEntityMemory(llm=llm, k=K)
        else:

             
            entity_memory_dict = buf_memory
            print(f'\n\nGetMemory from DB: {entity_memory_dict}\n\n')


            memory = ConversationEntityMemory(llm=llm, k=K, store=entity_memory_dict)
            # memory = entity_memory_dict

        
        # memory.entity_store.store

        # def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:


            #   ("Bandung", "Bandung adalah kota yang indah")

        
        print(f'\n\nGetMemory from DB: {memory}\n\n')
         
            #simpan entity memory ke record user
            # entity_memory = ConversationEntityMemory(llm=llm, k=K, store=entity_memory_dict)
        
 
        # Create the ConversationChain object with the specified configuration
        Conversation = ConversationChain(llm=llm,
                                       prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                                       memory=memory,
                                       verbose=True)
    
        output = Conversation.predict(input=incoming_message)
        # buf_memory = Conversation.memory.entity_store.store
        buf_memory = Conversation.memory
        print(f'buf_memory: {buf_memory}')


        pprint(buf_memory)


        #Save updated entities to database
        with app.app_context():
            user_query = User.query.filter_by(phone_number=phone).first()

            if user_query is None:
                print(f"No user found with phone: {phone}")
            else:
                try:
                    
                    try:
                        # user_query.entity_memory = str(buf_memory)
                        buf_memory = buf_memory.__dict__
                    
                    except:
                        pass

                    user_query.entity_memory = str(buf_memory)


                    db_sqlalchemy.session.commit()
                    print(f"Successfully updated entity memory for user with phone: {phone}")
                except Exception as e:
                    print(f"Failed to update entity memory: {str(e)}")

            # user.entity_memory = str(entity_store)
            # db_sqlalchemy.session.commit()

            # # user = User.query.filter_by(phone_number=phone).first()

            print(f'\n\nEntity Store to DB: {user_query.entity_memory} -- Type: {type(user_query.entity_memory)}\n\n')
      
 

    return output
    
