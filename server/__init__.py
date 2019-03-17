from dotenv import load_dotenv
from flask import Flask, redirect
import logging
from connexion import App

# Load Environment Variables
load_dotenv('.flaskenv')
load_dotenv('.env')

app = App(__name__, specification_dir='./')
app.add_api('openapi.yaml')

logger = logging.getLogger()

@app.route('/')
@app.route('/api')
def index():
    return redirect('/api/ui')
