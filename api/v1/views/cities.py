#!/usr/bin/python3
"""module to handle cities views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State


@app_views.route('/states/<id>/cities', methods=['GET'])
def all_cities(id):
    """Gets all cities of an object
    """
    dict = storage.all(City)
    list = []
    for city in dict.values():
        if city.state_id == id:
            list.append(city.to_dict())
    if len(list) == 0:
        abort(404)
    else:
        return jsonify(list)


@app_views.route('/cities/<id>', methods=['GET'])
def a_city(id):
    """Gets a specified city object
    """
    city = storage.get(City, id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<id>', methods=['DELETE'])
def delete_city(id):
    """Deletes a city object
    """
    city = storage.get(City, id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<id>/cities', methods=['POST'])
def create_city(id):
    """Creates a city object
    """
    data = request.get_json()
    if data is not None:
        if "name" not in data.keys():
            abort(400, description="Missing name")

        state_id = storage.get(State, id)
        if state_id is not None:
            city = City(name=data["name"], state_id=id)
            storage.new(city)
            storage.save()
            response = make_response(jsonify(city.to_dict()), 201)
            response.headers["Content-Type"] = "application/json"
            return response
        abort(404)
    abort(400, description="Not a JSON")


@app_views.route('cities/<id>', methods=['PUT'])
def update_city(id):
    """Updates city
    """
    city = storage.get(City, id)
    if city is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                    setattr(city, key, value)
                    city.save()
            return jsonify(city.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
