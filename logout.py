import streamlit as st  


def run():
    
    st.markdown("""
                # Logout
                """)


    # Tombol logout
    logout_button = st.button('Logout')
    if logout_button:
        st.session_state['token'] = None
        st.session_state['logged_in'] = False
        st.experimental_rerun() # Refresh halaman