#!/usr/bin/python3
"""Module to register the blueprint and then it creates a
connection with Flask"""
from os import environ
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exc):
    """invokes close function of stotage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error handler"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host_name = environ['HBNB_API_HOST']
    puerto = environ['HBNB_API_PORT']
    app.run(host=host_name, port=puerto, threaded=True)
