import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
import os
 
from flask import jsonify
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_openapi3 import OpenAPI, Info
 

# === Database ==== 



info = Info(title="Odoo API", version="1.0.0")
app = OpenAPI(__name__, info=info, static_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'

db_sqlalchemy = SQLAlchemy(app)

class Message(db_sqlalchemy.Model):
    __tablename__ = "message"

    id = db_sqlalchemy.Column(db_sqlalchemy.Integer, primary_key=True)
    #message_id = db_sqlalchemy.Column(db_sqlalchemy.String, nullable=False)  # Add this line
    phone_number = db_sqlalchemy.Column(db_sqlalchemy.String(20), nullable=False)
    message = db_sqlalchemy.Column(db_sqlalchemy.Text, nullable=False)
    result = db_sqlalchemy.Column(db_sqlalchemy.Text, nullable=True)
    incoming = db_sqlalchemy.Column(db_sqlalchemy.Boolean, default=True)


    def __init__(self, phone_number, message, result=None, incoming=False):
        self.phone_number = phone_number
        self.message = message
        self.result = result
        self.incoming = incoming



# Fungsi untuk mengirim pesan WhatsApp menggunakan API Wablas
def send_whatsapp_message(phone_number, message):
    url = "https://pati.wablas.com/api/v2/send-message"
    token = os.environ[
    'WABLAS TOKEN']  # Mengambil token dari environment variable

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
      

    try:
        phone = data.get('phone', None)  # Mengambil nomor telepon pengirim pesan
        incoming_message = data.get('message', None)  # Mengambil isi pesan
        message = ""
        # messageType = data.get('messageType', None)  # Mengambil tipe pesan 

        if phone == "628112227980":
            data_str = ""
            for key, value in data.items():
                if value not in [None, ""]:
                    data_str += f"{key}: {value}" + "\n"  
            message = data_str
            
        else:
            message = ""



        #Check Token
        




        print(f'Pesan dikirim : {message}')
        
        send_whatsapp_message(phone, message)  # Mengirim respon ke pengirim pesan

        
        
        return jsonify({'status': 'success', 'phone': phone})

    except Exception as e:
        print(f"Error: {e}")
        raise
   


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
