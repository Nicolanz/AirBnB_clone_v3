#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Funtion to get the status of a function

    Returns:
        [json]: [status]
    """
    return jsonify(status='OK')
