from server import create_app
from os import getenv

if __name__ == '__main__':
    debug = getenv('FLASK_ENV') == 'development'
    app = create_app()
    app.run(debug=debug, host='127.0.0.1')
