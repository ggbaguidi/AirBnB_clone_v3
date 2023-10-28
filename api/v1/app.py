#!/usr/bin/python3
"""App module"""
from os import environ
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(args=None):
    """teardown_appcontext"""
    if args:
        pass
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Page not fund"""
    if error:
        pass
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    HBNB_API_HOST = environ.get("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = environ.get("HBNB_API_PORT", 5000)
    print(app.url_map)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
