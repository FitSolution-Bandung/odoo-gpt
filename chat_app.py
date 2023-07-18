import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import os


#test

def chat_app():
	
	
	#BODY
	# Set up the Streamlit app layout
	st.title("🤖 Odoo-GPT")
	st.subheader("Integrasi Odoo-Whatsapp dengan optimalisasi GPT-3.5")
	
	# Ask the user to enter their OpenAI API key
	API_O = st.sidebar.text_input("API-KEY", type="password")
	
	if API_O == "":
	  # API_O = os.environ['OPENAI_KEY']
	  
	  API_O = os.environ['OPENAI_KEY']
	  st.info(f"""
				Saat ini menggunakan API-KEY default.             
				""")
	
	with st.expander("📝 ENTITY_MEMORY_CONVERSATION_TEMPLATE", expanded=False):
	  st.write(ENTITY_MEMORY_CONVERSATION_TEMPLATE)
	  st.write(ConversationEntityMemory)
	
	# Session state storage would be ideal
	if API_O:
	  # Create an OpenAI instance
	  llm = ChatOpenAI(temperature=0,
	               openai_api_key=API_O,
	               model_name=MODEL,
	               verbose=False)
	
	  # Create a ConversationEntityMemory object if not already created
	  if 'entity_memory' not in st.session_state:
	    st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K)
	
	  # Create the ConversationChain object with the specified configuration
	  Conversation = ConversationChain(llm=llm,
	                                   prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
	                                   memory=st.session_state.entity_memory)
	else:
	  st.sidebar.warning(
	    'API key required to try this app.The API key is not stored in any form.')
	  # st.stop()
	
	#Kirim Pesan
	chat_history_expander = st.expander("💬 Chat History", expanded=True)
	chat_history_expander.empty()
	
	user_input = st.chat_input(placeholder="Ketik pesan disini ...")
	
	#with st.expander("💬 Chat History", expanded=True):
	with chat_history_expander:
	  if user_input:
	    show_chat_histories(user_input)