#!/usr/bin/python3
""" Script that creates APIs with flask"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """ a function that ends database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ a function that handles 404 errors """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, debug=True, threaded=True)
