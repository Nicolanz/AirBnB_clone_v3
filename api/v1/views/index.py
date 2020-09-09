#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """Funtion to get the status of a function
    """
    return jsonify(status='OK')


@app_views.route('/stats')
def stats():
    """Endpoint that retrieves the number of
    each objects by type"""
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)})
