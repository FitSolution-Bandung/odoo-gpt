import streamlit as st  
import utils.login as login
import utils.logout as logout

from utils.database import User, Message, app, db_sqlalchemy




def run():
    # with app.app_context():
    #     message = Message.query.all()
        

    st.markdown("""
        # Database Viewer
    """)
    
    

    with app.app_context():
        users = User.query.all()
        massages = Message.query.all()



    with st.expander("Database Message"):
        st.markdown(f"""
            ### Table: 'message'""")
        st.write('**User:**\n\n')
        st.write(users)
        st.write('**Massage:**\n\n')    
        st.write(massages)    
        

 

   




if st.session_state.get('token') is None:
    st.warning("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
 
    # for param in st.session_state:
    #     st.write(param, st.session_state[param])
    logout.run()