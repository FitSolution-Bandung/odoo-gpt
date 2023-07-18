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
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os
import chat_app





# Set Streamlit page configuration
st.set_page_config(page_title='Odoo-GPT',
                   layout='wide',
                   initial_sidebar_state='auto')
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


# Define function to start a new chat
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


def show_chat_histories(user_input):

  output = Conversation.run(input=user_input)

  st.session_state["past"].append(user_input)
  st.session_state["generated"].append(output)

  past = st.session_state["past"]
  generated = st.session_state["generated"]
  download_str = st.session_state["download_str"]

  user = "user"
  bot = "Odoo-GPT"

  if len(past) > 0:
    for i in range(0, len(past)):
      with st.chat_message(user):
        st.write(past[i])

      with st.chat_message(bot):
        st.write(generated[i])

  else:
    st.info("No conversation history yet.")


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




body = chat_app()




#SIDEBAR
# Display stored conversation sessions in the sidebar
if st.session_state['past'] and st.session_state['generated']:
  st.sidebar.button("New Chat", on_click=new_chat, type='primary')

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