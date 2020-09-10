#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.user import User


@app_views.route('/users', methods=['GET'])
def all_user():
    """Get all User objects
    """
    dict = storage.all(User)
    list = []
    for user in dict.values():
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route('/users/<id>', methods=['GET'])
def a_user(id):
    """Get an User specific object
    """
    user = storage.get(User, id)
    if user is not None:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    """Delete an User object
    """
    user = storage.get(User, id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates an User object
    """
    data = request.get_json()
    if data is not None:
        if "email" not in data.keys():
            abort(400, description="Missing email")
        if "password" not in data.keys():
            abort(400, description="Missing password")
        user = User(email=data['email'], password=data['password'])
        for key, value in data.items():
            if key in ["first_name", "last_name"]:
                setattr(user, key, value)
        storage.new(user)
        storage.save()
        response = make_response(jsonify(user.to_dict()), 201)
        response.headers["Content-Type"] = "application/json"
        return response
    abort(400, description="Not a JSON")


@app_views.route('/users/<id>', methods=['PUT'])
def update_user(id):
    """Updates an User object
    """
    user = storage.get(User, id)
    if user is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at', 'email']:
                    setattr(user, key, value)
                    user.save()
            return jsonify(user.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
