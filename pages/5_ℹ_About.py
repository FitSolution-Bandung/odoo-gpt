import streamlit as st
import socket
 


def check_server(address, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Attempting to connect to {address} on port {port}")

    try:
        # Try to connect
        s.connect((address, port))
        print(f"Connected to {address} on port {port}")

        



        return True
    except socket.error as e:
        print(f"Connection to {address} on port {port} failed: {e}")
        return False
    finally:
        s.close()





#tampilkan localhost:80 dengan component html
url = 'http://localhost:80'
# components.iframe(url)\
st.components.v1.iframe(url, height=500, scrolling=True)






# if 'entity_memory' not in st.session_state:

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    status_login = st.session_state['logged_in']
    
else:
    st.warning("You are not logged in!")




 # Membuat socket
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     # Bind socket ke alamat dan port
#     s.bind(('localhost', 80))
#     # Mulai mendengarkan koneksi
#     s.listen()
    
#     # Menerima koneksi
#     conn, addr = s.accept()

#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             # Menerima data dari client
#             data = conn.recv(1024)
#             # Jika tidak ada data, hentikan loop
#             if not data:
#                 break
#             # Tampilkan data yang diterima
#             st.write(f"Received: {data.decode('utf-8')}")
#             # Kirim balasan ke client
#             conn.sendall(data)



server_running = check_server('127.0.0.1', 80)
    
if server_running:
    st.success('Server is running on port 80')
else:
    st.error('Server is not running on port 80')


st.markdown("""
# About Odoo-GPT

Odoo-GPT adalah aplikasi berbasis AI yang memadukan kekuatan Odoo, platform ERP (Enterprise Resource Planning) open-source yang populer, dengan GPT (Generative Pretrained Transformer), model bahasa AI canggih dari OpenAI.

## Fitur Utama

- **Integrasi Odoo**: Dengan Odoo sebagai dasar, Odoo-GPT dapat dengan mudah berintegrasi dengan berbagai modul Odoo seperti penjualan, pembelian, inventaris, akuntansi, dan banyak lagi.
- **Kekuatan GPT**: Dengan GPT, Odoo-GPT dapat memahami dan menghasilkan teks dalam bahasa alami, membuka berbagai kemungkinan baru untuk interaksi pengguna dan otomatisasi.

## Kenapa Odoo-GPT?

- **Efisiensi**: Otomatisasi berbasis AI dapat menghemat waktu dan upaya, mengurangi kesalahan manual, dan meningkatkan efisiensi operasional.
- **Fleksibilitas**: Dengan kemampuan untuk memahami dan menghasilkan bahasa alami, Odoo-GPT dapat digunakan dalam berbagai skenario, dari layanan pelanggan hingga analisis data.
- **Open Source**: Baik Odoo dan GPT adalah proyek open-source, yang berarti bahwa Odoo-GPT dapat dengan mudah disesuaikan dan diperluas sesuai kebutuhan Anda.

Untuk informasi lebih lanjut tentang Odoo-GPT, silakan hubungi kami melalui [email](mailto:info@odoo-gpt.com) atau kunjungi [website kami](http://www.odoo-gpt.com).
""")

