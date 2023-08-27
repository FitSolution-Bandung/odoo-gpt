import streamlit as st  
import utils.login as login
import utils.logout as logout
import time

from utils.database import User, Message, app, db_sqlalchemy, inspect_db
from utils import sidebar as sidebar
import pandas as pd

import json
from PyPDF2 import PdfReader
import pickle

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI

from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
from dotenv import load_dotenv
import base64



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.credentials/erp-2017-d844ca1fcc74.json'
load_dotenv('.credentials/.env')
MODEL = 'gpt-3.5-turbo'
API_O = os.environ['OPENAI_KEY']






def run():
    sidebar.run()
    mobile_phone =  st.session_state["mobile_phone"]
    
    st.markdown("""
        # Chat with PDF Document
    """)



    #Mempersiapkan folder untuk menyimpan file Document
    PKL_FOLDER = "static/documents/pkl"
    if not os.path.exists(PKL_FOLDER):
        os.makedirs(PKL_FOLDER)
    
    # Mengunggah file PDF
    pdf = st.file_uploader("Upload your PDF", type='pdf')

     
    if pdf is not None:
        # st.write(type(pdf))
        pdf_reader = PdfReader(pdf)
        text = "".join(page.extract_text() for page in pdf_reader.pages)

        # Memecah teks menjadi potongan-potongan yang dapat dikelola
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text=text)


        with st.expander(f"**{pdf.name}** : {len(pdf_reader.pages)} halaman"):
            st.write(chunks)

        # if st.button("Load Vector Store"):



        # Menyimpan nama file PDF
        store_name = pdf.name[:-4]
        pkl_path = os.path.join(PKL_FOLDER, f"{store_name}.pkl")

         # Memeriksa apakah embeddings sudah ada
        if os.path.exists(pkl_path):
            with open(pkl_path,"rb") as f:
                vectorstore = pickle.load(f)
                print(f'Vector Strore is Exist = {str(vectorstore)}')

        else:
            print(f'Get Embedding from OpenAI({len(chunks)} chunks)')
            embeddings = OpenAIEmbeddings(openai_api_key=API_O)

            vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
            try:
                with open(pkl_path, "wb") as f:
                    pickle.dump(vectorstore, f)
            except Exception as e:
                st.write(f"Error saving file: {e}")
            

         

        with st.expander(f"**{f}**"):
            st.write(vectorstore)


        # Menerima pertanyaan dari pengguna
        query = st.text_input("Ajukan pertanyaan tentang terkait file pdf unggahan Anda")

        if query:
           
            docs = vectorstore.similarity_search(query=query, k=5)

            # docs = vectorstore.similarity_search(query=query, )

            with st.expander(f"**Similarity Search** : {len(docs)} dokumen"):
                st.write(docs)
            
            
            llm = ChatOpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL)
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(f'Output = {response}')
                
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (IDR): IDR {cb.total_cost*15000}")



            st.write(response)
         
       
        



                        # st.success("Records from Table " + str(i+1) + " are deleted")
                        # time.sleep(1) # wait some time then refresh the page
                        # st.experimental_rerun()


if st.session_state.get('token') is None:
    st.error("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
