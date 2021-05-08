#!/usr/bin/python3
"""View for Amenity objects"""

from models import storage
from models.state import State
from models.city import City
from models.city import Amenity
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """Retrieve all Amenities based on state_id"""
    all_amenities = storage.all(Amenity).values()
    return jsonify([obj.to_dict() for obj in all_amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id=None):
    """Retrieve one Amenity based on amenity_id"""
    obj_amenity = storage.all(Amenity)
    for key, value in obj_amenity.items():
        key_split = key.split(".")
        if amenity_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Delete Amenity based on amenity_id"""
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity:
        key = 'Amenity' + "." + obj_amenity.id
        obj_amenity.delete()
        storage.save()
        return({})
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates an Amenity based on json"""
    # transform the HTTP body request to a dictionary
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if 'name' in obj_dict.keys():
        obj_amenity = Amenity(**obj_dict)
        obj_amenity.save()
        return jsonify(obj_amenity.to_dict()), 201
    else:
        abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update Amenity based on amenity_id"""
    obj_amenity = storage.get(Amenity, amenity_id)

    # These keys cannot be update
    ignore_keys = ['id', 'created_at', 'updated_at']

    # transform the HTTP body request to a dictionary
    to_update = request.get_json()
    if to_update is None:
        abort(400, 'Not a JSON')
    # check if key in dictionary is not allowed to be updated
    for key_ignore in ignore_keys:
        if key_ignore in to_update.keys():
            del to_update[key_ignore]
    if obj_amenity:
        for key, value in to_update.items():
            setattr(obj_amenity, key, value)
        obj_amenity.save()
        return jsonify(obj_amenity.to_dict())
    else:
        abort(404)
