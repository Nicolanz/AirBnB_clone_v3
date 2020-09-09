#!/usr/bin/python3
"""Module to register the blueprint and the it creates a
connection with Flask"""
from os import environ
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exc):
    """invokes close function of stotage

    Args:
        exc ([type]): [argument]
    """
    storage.close()

if __name__ == "__main__":
    host_name = environ['HBNB_API_HOST']
    puerto = environ['HBNB_API_PORT']
    app.run(host=host_name, port=puerto, threaded=True)
