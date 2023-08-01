import streamlit as st  
import utils.login as login
import utils.logout as logout
import time

from utils.database import User, Message, app, db_sqlalchemy, inspect_db
from utils import sidebar as sidebar
import pandas as pd




def run():
    sidebar.run()
    

    st.markdown("""
        # Database Viewer
    """)
    


    #check tables
    data = inspect_db()
    
    for i, data in enumerate(data):
        print(f'data[{i}] = {data}')

        with app.app_context():

            model = globals()[data.capitalize()] # Mendapatkan kelas model berdasarkan nama tabel
            records = model.query.all()
          
            print(f"All records for table {model}:")
        
            with st.expander(f"**Table {str(i+1)}:  {data.capitalize()}**"):

                # Create a list to store the records selected for deletion
                records_to_delete = []
                record_ids_to_delete = []

                for record in records:
                    # st.write(record)
                        
                    # Add a checkbox for each record
                    # if st.checkbox(f"🗑️ Select **{data.capitalize()} {record.id}** for deletion"):
                    if st.checkbox(f"🗑️ {record}"):
                        records_to_delete.append(record)
                        record_ids_to_delete.append(record.id)
                
                # Add a delete button for the selected records
                if len(record_ids_to_delete) > 0:

                    if st.button(f"❌ DELETE records of **{data.capitalize()}**  with id: {record_ids_to_delete}"):
                        for record in records_to_delete:
                            db_sqlalchemy.session.delete(record)
                            db_sqlalchemy.session.commit()
                            st.success(f"Record {record.id} deleted")
                        time.sleep(1) # wait some time then refresh the page
                        st.experimental_rerun()
                    

                st.write("---")

                if st.checkbox(f"⚠️ **EMPTY** the **'{data.capitalize()}'** table."):
                    if st.button(f"I am sure to EMPTY the **'{data.capitalize()}'** table."):
                        
                        model.query.delete()  # Menghapus semua baris dari tabel
                        # db_sqlalchemy.session.delete(data)
                        db_sqlalchemy.session.commit()
                        st.success("Table " + str(i+1) + " deleted")
                        time.sleep(1) # wait some time then refresh the page
                        st.experimental_rerun()




                    # if st.checkbox(f"🗑️ Delete **{data.capitalize()} {record.id}**"):
                    #    if st.button(f"I am sure to DELETE: {data.capitalize()} {record.id}"):
                        
                    #         db_sqlalchemy.session.delete(record)
                    #         db_sqlalchemy.session.commit()
                    #         st.success(f"Record {record.id} deleted")
                    #         time.sleep(1) #tunggu beberapa saat kemudian refrsh halaman
                    #         st.experimental_rerun()
                            
                    # print(record)


            


    # #definisikan "data" sebagai penampungan dalam bentuk list
    # data = []
    # print(f'data = {data}')

    # with app.app_context():
    #     data.append(User.query.all())
    #     data.append(Message.query.all())

    #     # data[1] = User.query.all()
    #     # data[2] = Message.query.all()


   

    # for i, data in enumerate(data):
    #     print(f'data[{i}] = {data}')


    #     with st.expander("Table " + str(i+1)):
    #         st.write(data)

    #         #buat tombol delete untuk setiap i 
    #         if st.button("Delete Table " + str(i+1)):
    #             with app.app_context():
    #                 db_sqlalchemy.session.delete(data)
    #                 db_sqlalchemy.session.commit()
    #                 st.success("Table " + str(i+1) + " deleted")

    


 

   




if st.session_state.get('token') is None:
    st.error("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
 
   