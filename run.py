from os import environ
from waitress import serve
from Cooking import app

port = int(environ.get('PORT', 5000))

if __name__ == "__main__":
    #app.run(environ.get('PORT'))
    serve(app, host = '0.0.0.0', port=port)
