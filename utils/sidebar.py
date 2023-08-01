import streamlit as st
from utils import logout

def run():
    # Tombol 'logout' di sidebar
    with st.sidebar.container():
        
        logout.run()
       


    