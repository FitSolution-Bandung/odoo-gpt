# app.py
from flask import Flask, request
import os
import threading
import streamlit as st

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def respond():
	print(request.json)
	return {'status': 'success'}


# def run_flask():
# 	app.run(port=80)


# threading.Thread(target=run_flask).start()


# def run_streamlit():
# 	os.system("streamlit run login.py")


# threading.Thread(target=run_streamlit).start()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)