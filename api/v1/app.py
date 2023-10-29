#!/usr/bin/python3
""" a script that creates apis with flask"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    """ a function that ends database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ a function that handles 404 errors """
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    app.run(host, port, debug=True, threaded=True)
