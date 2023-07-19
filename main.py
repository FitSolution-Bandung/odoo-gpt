from flask import Flask, request
import os
import threading
import streamlit as st

app = Flask(__name__)


@app.route('/webhook', methods=['POST', 'GET'])
def respond():
    if request.method == 'POST':
        print(request.json)
    return {'status': 'success'}

@app.route('/')
def hello_world():
    return 'Hello, World!'

def run_flask():
    app.run(port=5000)


threading.Thread(target=run_flask).start()


def run_streamlit():
    os.system("streamlit run Menu.py --server.port 8500")


threading.Thread(target=run_streamlit).start()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=80)