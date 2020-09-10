#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def all_place(city_id):
    """Get all Place objects
    """
    city = storage.get(City, city_id)
    if city is not None:
        dict = storage.all(Place)
        list = []
        for place in dict.values():
            if place.city_id == city.id:
                list.append(place.to_dict())
        return jsonify(list)
    abort(404)


@app_views.route('/places/<id>', methods=['GET'])
def a_place(id):
    """Get a Place specific object
    """
    place = storage.get(Place, id)
    if place is not None:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<id>', methods=['DELETE'])
def delete_place(id):
    """Delete a Place object
    """
    place = storage.get(Place, id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place object
    """
    city = storage.get(City, city_id)
    if city is not None:
        data = request.get_json()
        if data is not None:
            if "user_id" not in data.keys():
                abort(400, description="Missing user_id")
            user = storage.get(User, data["user_id"])
            if user is not None:
                if "name" not in data.keys():
                    abort(400, description="Missing name")
                place = Place(city_id=city_id,
                              user_id=data["user_id"],
                              name=data["name"])
                for key, value in data.items():
                    if key in ["number_rooms", "number_bathrooms",
                               "max_guest", "price_by_night", "latitude",
                               "longitude", "description"]:
                        setattr(place, key, value)
                storage.new(place)
                storage.save()
                response = make_response(jsonify(place.to_dict()), 201)
                response.headers["Content-Type"] = "application/json"
                return response
            abort(404)
        abort(400, description="Not a JSON")
    abort(404)


@app_views.route('/places/<id>', methods=['PUT'])
def update_palce(id):
    """Updates a Place object
    """
    place = storage.get(Place, id)
    if place is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'user_id', 'city_id',
                               'created_at', 'updated_at']:
                    setattr(place, key, value)
                    place.save()
            return jsonify(place.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
