#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/states', methods=['GET'])
def all_states():
    """Get all State objects
    """
    dict = storage.all(State)
    list = []
    for state in dict.values():
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route('/states/<id>', methods=['GET'])
def a_state(id):
    """Get an specific object
    """
    state = storage.get(State, id)
    if state is not None:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """Deletes an object
    """
    state = storage.get(State, id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates an object
    """
    data = request.get_json()
    if data is not None:
        if "name" not in data.keys():
            abort(400, description="Missing name")
        state = State(name=data["name"])
        storage.new(state)
        storage.save()
        response = make_response(jsonify(state.to_dict()), 201)
        response.headers["Content-Type"] = "application/json"
        return response
    abort(400, description="Not a JSON")


@app_views.route('/states/<id>', methods=['PUT'])
def update_state(id):
    """Updates an object
    """
    state = storage.get(State, id)
    if state is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
                    state.save()
            return jsonify(state.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
