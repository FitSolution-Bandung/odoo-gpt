import sqlite3
import streamlit as st  

#Drop table
def drop_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    con.commit()
    
    print(f"Table '{table_name}' has been dropped.")
        
    con.close()


#drop_table('user_data.db', 'users')
# drop_table('user_data.db', 'message')
    
#Lihat isi  database di sqlite
def view_tables(db_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        st.write(f"Table name: {table[0]}")
        print(f"Table name: {table[0]}")

     
        
    con.close()

# view_tables('user_data')



#Lihat isi table
def view_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    
    for row in rows:
        st.write(row)
        print(row)
   
    con.close()

# view_table('user_data.db', 'users')



#Hapus semua isi table
def clear_table(db_name, table_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    cursor.execute(f"DELETE FROM {table_name};")
    con.commit()
    
    print("All rows deleted from table 'user'")
    
    con.close()

# clear_table('user.db', 'users')


def add_column(column_to_add):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()

    # Menambahkan kolom mobile_phone
    c.execute(f"ALTER TABLE users ADD COLUMN {column_to_add} text")

    conn.commit()
    conn.close()

# add_mobile_phone_column()
# clear_table('user_data.db', 'users')
# add_column('username')