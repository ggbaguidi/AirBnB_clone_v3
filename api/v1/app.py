#!/usr/bin/python3
"""App module"""
from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(args=None):
    """app teardown"""
    if args:
        pass
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = environ.get("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = environ.get("HBNB_API_PORT", 5000)
    print(app.url_map)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
