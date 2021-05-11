#!/usr/bin/python3
"""View fo User objects"""

from models import storage
from models.city import City
from models.review import Review
from models.place import Place
from models.user import User
from models.amenity import Amenity
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities_places(place_id):
    """Retrieve all amenities based on place_id"""
    obj_places = storage.get(Place, place_id)
    list_amenities = []
    if obj_places is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_obj = obj_places.amenities
    else:
        amenity_obj = obj_places.amenity_ids
    for amenity in amenity_obj:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_places(place_id, amenity_id):
    """Delete a review based on review_id"""
    obj_review = storage.get(Review, review_id)
    if obj_review:
        obj_review.delete()
        storage.save()
        return({})
    abort(404)
