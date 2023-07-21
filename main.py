from flask import Flask, request, render_template
import os
import threading
import streamlit as st
 

# ======= STREAMLIT =======

def run_streamlit():
    os.system("streamlit run Menu.py --server.port 8500")
threading.Thread(target=run_streamlit).start()



# ======= FLASK =======


app = Flask(__name__)


@app.route('/')
def home():
    url = 'http://localhost:8500'
    return render_template('index.html', url=url)



@app.route('/webhook', methods=['POST', 'GET'])
def respond():
    if request.method == 'POST':
        print(request.json)
    return {'status': 'success'}



def run_flask():
    #app.run(port=5000)
    app.run(host='0.0.0.0', port=80)


threading.Thread(target=run_flask).start()


