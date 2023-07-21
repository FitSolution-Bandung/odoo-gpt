import sqlite3
import streamlit as st  



    
#Lihat isi  database di sqlite
def view_tables(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        st.write(f"Table name: {table[0]}")
        
    con.close()

#Lihat isi table
def view_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        st.write(row)
   
    con.close()



#Hapus semua isi table
def clear_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    cursor.execute(f"DELETE FROM {table_name};")
    con.commit()
    
    print("All rows deleted from table 'user'")
    
    con.close()





