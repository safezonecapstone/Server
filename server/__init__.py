from dotenv import load_dotenv
from flask import redirect
import logging
from connexion import FlaskApp
from flask_cors import CORS

# Load Environment Variables
load_dotenv('.flaskenv')
load_dotenv('.env')

app = FlaskApp(__name__, specification_dir='./')
app.add_api('openapi.yaml')

CORS(app.app)

logger = logging.getLogger()

@app.route('/')
@app.route('/api')
def index():
    return redirect('/api/ui')
