#!/usr/bin/python3
"""module to handle cities views"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Gets all amenity objects
    """
    dict = storage.all(Amenity)
    list = []
    for amenity in dict.values():
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<id>', methods=['GET'])
def a_amenity(id):
    """Gets an specified amenity object
    """
    amenity = storage.get(Amenity, id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<id>', methods=['DELETE'])
def delete_amenity(id):
    """Deletes a amenity object
    """
    amenity = storage.get(Amenity, id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an amenity object
    """
    data = request.get_json()
    if data is not None:
        if "name" not in data.keys():
            abort(400, description="Missing name")
        amenity = Amenity(name=data["name"])
        storage.new(amenity)
        storage.save()
        response = make_response(jsonify(amenity.to_dict()), 201)
        response.headers["Content-Type"] = "application/json"
        return response
    abort(400, description="Not a JSON")


@app_views.route('/amenities/<id>', methods=['PUT'])
def update_amenity(id):
    """Updates amenity
    """
    amenity = storage.get(Amenity, id)
    if amenity is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
                    amenity.save()
            return jsonify(amenity.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
