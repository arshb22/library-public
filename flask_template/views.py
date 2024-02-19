from flask import Flask, redirect, url_for, render_template, request, jsonify, session, send_file
from flask_app import app
import os
import pandas as pd
import openai 
import json
from dotenv import load_dotenv
from openai import OpenAI 

load_dotenv()

api_key = os.environ.get("OPEN_AI_API_KEY")
client = openai.Client(api_key=api_key)

@app.route('/')
def home():
    session['chat_history'] = []
    session['current_step'] = 0
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
