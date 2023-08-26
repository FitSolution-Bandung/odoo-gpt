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
    
    # Mengunggah file PDF
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        # st.write(type(pdf))
        pdf_reader = PdfReader(pdf)
        text = "".join(page.extract_text() for page in pdf_reader.pages)

        # Memecah teks menjadi potongan-potongan yang dapat dikelola
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_text(text=text)

        with st.expander(f"**PDF Text**"):
            st.write(chunks)

        # Menyimpan nama file PDF
        store_name = pdf.name[:-4]

         # Memeriksa apakah embeddings sudah ada
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl","rb") as f:
                vectorstore = pickle.load(f)

                print(f'Vector Strore = {str(vectorstore)}')

        else:
            embeddings = OpenAIEmbeddings(openai_api_key=API_O)
            print(f'Embedding chunks... with {len(chunks)} chunks')

            vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl","wb") as f:
                pickle.dump(vectorstore, f)


        # Menerima pertanyaan dari pengguna
        query = st.text_input("Ask questions about related your upload pdf file")

        if query:
           


            docs = vectorstore.similarity_search(query=query, k=3)
            llm = OpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL)
            chain = load_qa_chain(llm=llm, chain_type="stuff")

            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(f'Output = {response}')
                print(f'Callback = {cb}')
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
 
   