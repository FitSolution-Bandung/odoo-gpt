from datetime import datetime
from utils.database import Message, User, db_sqlalchemy, app, write_chat_to_db
import streamlit as st

import utils.whatsapp_agent as wa_agent




def show_chat_histories(phone_number, user_input=None, **kwargs):
      
    print(f'nomor telp user: {phone_number}')
    output = ""
    total_cost = 0.0


    with app.app_context():
      # messages = Message.query.all()

      messages = Message.query.filter_by(recipient=phone_number).order_by(Message.id).all()
      user = User.query.filter_by(phone_number=phone_number).first()

    past = []
    generated = []

    for message in messages:
        past.append(message.past)
        generated.append(message.generated)

    if len(messages) > 0:
        for i in range(0, len(messages)):
            with st.chat_message(name="User", avatar="🧑‍💻"):
                st.write(f"{past[i]}")

            with st.chat_message(name="Odoo-GPT", avatar="🤖"):
                    st.write(f"{generated[i]}")

    if user_input:
        with st.chat_message(name="User", avatar="🧑‍💻"):
           st.write(user_input)

        with st.chat_message(name="Odoo-GPT", avatar="🤖"):
            with st.spinner("Memuat Respon ..."):
                # output = Conversation.run(input=user_input)
                # output = wa.prepare_message(phone_number, user_input)

                output, total_cost = wa_agent.predict_gpt(phone_number, user_input)

            st.write(output)


        # Tambahkan pesan pengguna dan respon bot ke database
        # write_chat_to_db(recipient, past, sender, generated)
     
        past = user_input
        recipient = phone_number
      

        #Check parameter di *args, **kwargs
        sender = kwargs.get('sender', "Odoo-GPT")       
        

        write_chat_to_db(user.username, recipient, past, sender, output, total_cost)
      
    return phone_number
