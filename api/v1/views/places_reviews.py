#!/usr/bin/python3
"""View fo User objects"""

from models import storage
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieve all reviews based on place_id"""
    obj_places = storage.get(Place, place_id)
    list_reviews = []
    if obj_places:
        for review in obj_places.reviews:
            list_reviews.append(review.to_dict())
        return jsonify(list_reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review(review_id):
    """Retrieve a review based on review_id"""
    obj_review = storage.get(Review, review_id)
    if obj_review:
        return jsonify(obj_review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Delete a review based on review_id"""
    obj_review = storage.get(Review, review_id)
    if obj_review:
        obj_review.delete()
        storage.save()
        return({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Post review based on json"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    # transform the HTTP body request to a dictionary
    if 'user_id' not in obj_dict:
        abort(400, 'Missing user_id')
    user_id = obj_dict.get('user_id', None)
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'text' not in obj_dict:
        abort(400, 'Missing text')
    obj_review = Review(place_id=place_id, **obj_dict)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates review based on user_id"""
    obj_review = storage.get(Review, review_id)
    if obj_review is None:
        abort(404)
    # transform the HTTP body request to a dictionary
    to_update = request.get_json()
    if to_update is None:
        abort(400, 'Not a JSON')

    # These keys cannot be update
    ignore_keys = ['id', 'user_id', 'place_id',
                   'created_at', 'updated_at']

    # check if key in dictionary is not allowed to be updated
    for key_ignore in ignore_keys:
        if key_ignore in to_update.keys():
            del to_update[key_ignore]
    if obj_review:
        for key, value in to_update.items():
            setattr(obj_review, key, value)
        obj_review.save()
        return jsonify(obj_review.to_dict()), 200
    else:
        abort(404)
