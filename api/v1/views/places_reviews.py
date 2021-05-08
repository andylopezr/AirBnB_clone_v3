#!/usr/bin/python3
"""View fo User objects"""

from models import storage
from models.review import Review
from models.place import Place
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
def one_review(review_id=None):
    """Retrieve a review based on review_id"""
    obj_review = storage.all(Review)
    for key, value in obj_review.items():
        key_split = key.split(".")
        if review_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """Delete a review based on review_id"""
    obj_review = storage.get(Review, review_id)
    if obj_review:
        key = 'User' + "." + obj_review.id
        obj_review.delete()
        obj_review.save()
        return({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Post review based on json"""
    # transform the HTTP body request to a dictionary
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)
    if 'user_id' not in obj_dict.keys():
        abort(400, 'Missing user_id')
    if 'text' not in obj_dict.keys():
        abort(400, 'Missing text')
    obj_review = Review(user_id=user_id, **obj_dict)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates User based on user_id"""
    obj_review = storage.get(Review, review_id)

    # These keys cannot be update
    ignore_keys = ['id', 'user_id', 'place_id',
                   'created_at', 'updated_at']

    # transform the HTTP body request to a dictionary
    to_update = request.get_json()
    if to_update is None:
        abort(400, 'Not a JSON')
    # check if key in dictionary is not allowed to be updated
    for key_ignore in ignore_keys:
        if key_ignore in to_update.keys():
            del to_update[key_ignore]
    if obj_review:
        for key, value in to_update.items():
            setattr(obj_review, key, value)
        obj_review.save()
        return jsonify(obj_review.to_dict())
    else:
        abort(404)