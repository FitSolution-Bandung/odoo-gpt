import streamlit as st  
import utils.login as login
import utils.logout as logout
import time

from utils.database import User, Message, app, db_sqlalchemy, inspect_db
from utils import sidebar as sidebar
import pandas as pd

import json



def run():
    sidebar.run()
    mobile_phone =  st.session_state["mobile_phone"]
    
    st.markdown("""
        # Database Viewer
    """)
    see_all_records = st.checkbox("See All Records")
    
    #definiskan list option dari database user field phone_number
    with app.app_context():
        options = [user.phone_number for user in User.query.all()]
        print(f"options = {options}")
        selected_number = st.multiselect('Filter dengan Nomor Telp:', options)
        selected_number.append(mobile_phone)

    #check tables
    data = inspect_db()

    print(f"Data = {data}")
    

    for i, data in enumerate(data):
        print(f'data[{i}] = {data}')

        with app.app_context():

            model = globals()[data.capitalize()] # Mendapatkan kelas model berdasarkan nama tabel

            #filter kalau hanya ingin melihat data milik sendiri
            if not see_all_records:
                if model == Message:
                    # records = model.query.filter_by(recipient=mobile_phone).all()
                    records = model.query.filter(model.recipient.in_(selected_number)).all()

                else:
                    # records = model.query.filter_by(phone_number=mobile_phone).all()
                    records = model.query.filter(model.phone_number.in_(selected_number)).all()

            else:
                records = model.query.all()
        
            with st.expander(f"**Table {str(i+1)}:  {data.capitalize()}  [{len(records)}]**"):

                # Create a list to store the records selected for deletion
                records_to_delete = []
                record_ids_to_delete = []

                for record in records:
            


                    if st.checkbox(f"🗑️ {record}"):
                        records_to_delete.append(record)
                        record_ids_to_delete.append(record.id)
                
                # Add a delete button for the selected records
                if len(record_ids_to_delete) > 0:

                    if st.button(f"❌ DELETE records of **{data.capitalize()}**  with id: {record_ids_to_delete}"):
                        for record in records_to_delete:
                            try :    
                                db_sqlalchemy.session.delete(record)
                                db_sqlalchemy.session.commit()
                                st.success(f"Record {record} deleted")
                            except:
                                st.error(f"Record {record} failed to delete")

                        time.sleep(1) # wait some time then refresh the page
                        st.experimental_rerun()
                    

                st.write("---")

                if st.checkbox(f"⚠️ **DELETE** from **'{data.capitalize()}'** table."):
                    
                    if not see_all_records:
                        button_text = f"**I am sure to DELETE** records with phone number [{mobile_phone}] of the **'{data.capitalize()}'** table."
                    else:
                        button_text = f"**I am sure to EMPTY** the **'{data.capitalize()}'** table."



                    if st.button(button_text):
                        
                        if not see_all_records:
                            if model == Message:
                                model.query.filter_by(recipient=mobile_phone).delete()  # Menghapus semua baris dari tabel
                            else:
                                model.query.filter_by(phone_number=mobile_phone).delete()
                        else:
                            model.query.delete()  # Menghapus semua baris dari tabel


                        # db_sqlalchemy.session.delete(data)
                        db_sqlalchemy.session.commit()
                        st.success("Records from Table " + str(i+1) + " are deleted")
                        time.sleep(1) # wait some time then refresh the page
                        st.experimental_rerun()


if st.session_state.get('token') is None:
    st.error("You are not logged in!")
    login.run()

else:

    #Tampilkan kredensial
    run()
 
   