#!/usr/bin/python3
""" Script that creates APIs with flask"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """ Module that ends database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Module that handles 404 errors """
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST')
    if not api_host:
        api_host = '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    app.run(api_host, port, debug=True, threaded=True)
