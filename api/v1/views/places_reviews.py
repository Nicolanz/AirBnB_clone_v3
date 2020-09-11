#!/usr/bin/python3
"""Routes status and returns it as JSON"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def all_reviews(place_id):
    """Get all Review objects
    """
    place = storage.get(Place, place_id)
    if place is not None:
        dict = storage.all(Review)
        list = []
        for review in dict.values():
            if review.place_id == place.id:
                list.append(review.to_dict())
        return jsonify(list)
    abort(404)


@app_views.route('/reviews/<id>', methods=['GET'])
def a_review(id):
    """Get a specific Review object
    """
    review = storage.get(Review, id)
    if review is not None:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<id>', methods=['DELETE'])
def delete_review(id):
    """Deletes a Review object
    """
    review = storage.get(Review, id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review object
    """
    place = storage.get(Place, place_id)
    if place is not None:
        data = request.get_json()
        if data is not None:
            if "user_id" not in data.keys():
                abort(400, description="Missing user_id")
            user = storage.get(User, data["user_id"])
            if user is not None:
                if "text" not in data.keys():
                    abort(400, description="Missing text")
                review = Review(place_id=place_id,
                                user_id=data["user_id"],
                                text=data["text"])
                storage.new(review)
                storage.save()
                response = make_response(jsonify(review.to_dict()), 201)
                response.headers["Content-Type"] = "application/json"
                return response
            abort(404)
        abort(400, description="Not a JSON")
    abort(404)


@app_views.route('/reviews/<id>', methods=['PUT'])
def update_review(id):
    """Updates a Review object
    """
    review = storage.get(Review, id)
    if review is not None:
        data = request.get_json()
        if data is not None:
            for key, value in data.items():
                if key not in ['id', 'user_id', 'place_id',
                               'created_at', 'updated_at']:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict())
        abort(400, description="Not a JSON")
    abort(404)
