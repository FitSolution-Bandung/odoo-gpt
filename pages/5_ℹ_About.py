import streamlit as st


# if 'entity_memory' not in st.session_state:

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    status_login = st.session_state['logged_in']
    
else:
    st.warning("You are not logged in!")



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

