#!/usr/bin/python3
"""View for place objects"""

from models import storage
from models.place import Place
from models.city import City
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieve all the places based on city_id"""
    # Retrieve state based on id
    obj_cities = storage.get(City, city_id)
    list_places = []
    if obj_cities:
        for place in obj_cities.places:
            list_places.append(place.to_dict())
        return jsonify(list_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def one_place(place_id=None):
    """Retrieve one place based on place_id"""
    obj_place = storage.all(Place)
    for key, value in obj_place.items():
        key_split = key.split(".")
        if place_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Delete place based on place_id"""
    obj_place = storage.get(Place, place_id)
    if obj_place:
        key = 'Place' + "." + obj_place.id
        obj_place.delete()
        storage.save()
        return({})
    abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place based on json"""
    # transform the HTTP body request to a dictionary
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "user_id" not in obj_dict:
        abort(400, 'Missing user_id')
    if "password" not in obj_dict:
        abort(400, 'Missing password')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'name' in obj_dict.keys():
        obj_place = Place(city_id=city_id, **obj_dict)
        obj_place.save()
        return jsonify(obj_place.to_dict()), 201
    else:
        abort(400, 'Missing name')


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates place based on place_id"""
    obj_place = storage.get(Place, place_id)

    # These keys cannot be update
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    # transform the HTTP body request to a dictionary
    to_update = request.get_json()
    if to_update is None:
        abort(400, 'Not a JSON')
    # check if key in dictionary is not allowed to be updated
    for key_ignore in ignore_keys:
        if key_ignore in to_update.keys():
            del to_update[key_ignore]
    if obj_place:
        for key, value in to_update.items():
            setattr(obj_place, key, value)
        obj_place.save()
        return jsonify(obj_place.to_dict())
    else:
        abort(404)
