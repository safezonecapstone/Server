from server import create_app
from os import getenv

debug = getenv('FLASK_ENV') == 'development'
app = create_app('../')

if __name__ == '__main__':
    app.run(debug=debug, host='127.0.0.1')
