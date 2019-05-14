from server import app
from os import getenv
from dotenv import load_dotenv

if __name__ == "__main__":
    debug = getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='127.0.0.1')
