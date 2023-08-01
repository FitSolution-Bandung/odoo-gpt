"""
Skrip Python ini mengintegrasikan paket perangkat lunak ERP, Odoo, dengan layanan pesan WhatsApp, 
menggunakan model bahasa generatif OpenAI, GPT-3.5, sebagai asisten AI. 
Dibangun dengan pustaka Streamlit, Langchain, dan llms, skrip ini memungkinkan interaksi 
berbasis percakapan yang kontekstual dan informatif antara sistem Odoo dan pengguna melalui WhatsApp, 
dengan asisten AI memfasilitasi dan memperkaya proses komunikasi.# Author: Avratanu Biswas

# July 2023
#by Andhitiawarman Nugraha
"""

# Import necessary libraries
import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from utils.get_credential import get_credentials, is_valid_token
 
import os
import textwrap

import utils.login as login
import utils.sidebar as sidebar
import utils.whatsapp as wa

from utils.database import Message, User, db_sqlalchemy, app, write_chat_to_db


  

def new_chat():
  """
    Clears session state and starts a new chat.
    """
  save = []
  for i in range(0, len(st.session_state['generated'])):
    save.append("User:" + st.session_state["past"][i])
    save.append("Odoo-GPT:" + st.session_state["generated"][i])

  st.session_state["stored_session"].append(save)
  st.session_state["generated"] = []
  st.session_state["past"] = []
  st.session_state["input"] = ""
  st.session_state.entity_memory.entity_store = {}
  st.session_state.entity_memory.buffer.clear()


def show_chat_histories(user_input=None):
      
      
      
    credentials= st.session_state['credentials']
    if credentials is not None:
        url, username, password, created_at, mobile_phone = credentials

        sender = mobile_phone



    with app.app_context():
      messages = Message.query.all()
    
    mobile_phones = set()
    for msg in messages:
       mobile_phones.add(msg.recipient) 
    
    print(f'nomor telp user: {mobile_phones}')

    for mobile_phone in mobile_phones:
       #Extract all messages from the database
        with app.app_context():
            messages = Message.query.filter_by(recipient=mobile_phone).order_by(Message.id).all()
            

        past = []
        generated = []

        for message in messages:
            past.append(message.past)
            generated.append(message.generated)




    if len(messages) > 0:
        for i in range(0, len(messages)):
            with st.chat_message(name="User", avatar="🧑‍💻"):
                st.write(f"{past[i]}")

            with st.chat_message(name="Odoo-GPT", avatar="🤖"):
                    st.write(f"{generated[i]}")
 
    if user_input:
        with st.chat_message(name="User", avatar="🧑‍💻"):
           st.write(user_input)

        with st.chat_message(name="Odoo-GPT", avatar="🤖"):
            with st.spinner("Memuat Respon ..."):
                # output = Conversation.run(input=user_input)
                output = wa.prepare_message(mobile_phone, user_input)

            st.write(output)


    # Tambahkan pesan pengguna dan respon bot ke database
    # write_chat_to_db(recipient, past, sender, generated)
     
        past = user_input
        recipient = mobile_phone
      
        write_chat_to_db(recipient, past, sender, output)
      


      # st.session_state["past"].append(user_input)
      # st.session_state["generated"].append(output)
   




def run():
    sidebar.run()


                     
    # Initialize session states
    if "generated" not in st.session_state:
      st.session_state["generated"] = []
    if "past" not in st.session_state:
      st.session_state["past"] = []
    if "input" not in st.session_state:
      st.session_state["input"] = ""
    if "stored_session" not in st.session_state:
      st.session_state["stored_session"] = []
    if "download_str" not in st.session_state:
      st.session_state["download_str"] = []
    if "token" not in st.session_state:
      st.session_state["token"] = []
    if "credentials" not in st.session_state:
      st.session_state["credentials"] = []

 


    # Define function to start a new chat
    
    # sidebar

    #SIDEBAR
    # Set up sidebar with various options
    with st.sidebar.expander("🛠️ ", expanded=False):
      # Option to preview memory store
      if st.checkbox("Preview memory store"):
        # st.expander("Memory-Store", expanded=False)
        st.session_state.entity_memory.store

      # Option to preview memory buffer
      if st.checkbox("Preview memory buffer"):
        # with st.expander("Bufffer-Store", expanded=False):
        st.session_state.entity_memory.buffer

      MODEL = st.selectbox(label='Model',
                           options=[
                             'gpt-3.5-turbo', 'text-davinci-003',
                             'text-davinci-002', 'code-davinci-002'
                           ])
      K = st.number_input(' (#)Summary of prompts to consider',
                          min_value=3,
                          max_value=1000)



    #BODY
    # Set up the Streamlit app layout
    
    # Ask the user to enter their OpenAI API key
    # API_O = st.sidebar.text_input("API-KEY", type="password")

    # if API_O == "":
    #   # API_O = os.environ['OPENAI_KEY']
      
    #   API_O = os.environ['OPENAI_KEY']
    #   st.info(f"""
    #       Saat ini menggunakan API-KEY default.             
    #       """)

    # with st.expander("📝 Debug Information", expanded=False):
    #   credentials = st.session_state['credentials']
    #   if credentials is not None:
    #     url, username, password, created_at, mobile_phone = credentials

    #   st.write(f'**ENTITY_MEMORY_CONVERSATION_TEMPLATE:**\n\n{str(ENTITY_MEMORY_CONVERSATION_TEMPLATE)}')
    #   st.write('---')
      
    #   debug = st.empty()


    # # Session state storage would be ideal
    # if API_O:
    #   # Create an OpenAI instance
    #   llm = ChatOpenAI(temperature=0,
    #                openai_api_key=API_O,
    #                model_name=MODEL,
    #                verbose=False)

      
    #   with debug:
        
    #     st.write(f'**ConversationEntityMemory(llm=llm, k=K):**\n\n{textwrap.fill(str(ConversationEntityMemory(llm=llm, k=K)))}')  



    #   # Create a ConversationEntityMemory object if not already created
    #   if 'entity_memory' not in st.session_state:
    #     st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)




    #   # Create the ConversationChain object with the specified configuration
    #   Conversation = ConversationChain(llm=llm,
    #                                    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    #                                    memory=st.session_state.entity_memory)
    # else:
    #     st.sidebar.warning(
    #       'API key required to try this app.The API key is not stored in any form.')
    #     st.stop()



    #Kirim Pesan
    chat_history_expander = st.expander("💬 Chat History", expanded=True)
    chat_history_expander.empty()

    user_input = st.chat_input(placeholder="Ketik pesan disini ...")

    #with st.expander("💬 Chat History", expanded=True):
    with chat_history_expander:
        # if user_input:
        show_chat_histories(user_input)




    #SIDEBAR
    # Display stored conversation sessions in the sidebar
    if st.session_state['past'] and st.session_state['generated']:
        st.sidebar.button("New Chat", on_click=new_chat, type='primary')
    
    st.sidebar.button("Call History Chat", on_click=show_chat_histories, type='primary')

    for i, sublist in enumerate(st.session_state.stored_session):
        with st.sidebar.expander(label=f"Conversation-Session:{i}"):
            st.write(sublist)
            st.download_button("Download Chat",
                               "\n".join(sublist),
                               file_name=f"chat-{i}.txt",
                               mime="text/plain")

    # Allow the user to clear all stored conversation sessions
    if st.session_state.stored_session:
      # if st.sidebar.checkbox("Clear-all"):
        if st.sidebar.button("Clear-all"):
            st.sidebar.checkbox("Klik disini untuk menghapus semuanya",
                                on_change=lambda: st.session_state.clear())
          
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    status_login = st.session_state['logged_in']
    run()
else:
    st.error("You are not logged in!")
    login.run()


