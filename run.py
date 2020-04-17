from os import environ
from Cooking import app


if __name__ == "__main__":
    app.run(environ.get('PORT'))
