#!/usr/bin/python3
"""View for City objects"""

from models import storage
from models.state import State
from models.city import City
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Retrieve all the cities based on state_id"""
    # Retrieve state based on id
    obj_state = storage.get(State, state_id)
    list_cities = []
    if obj_state:
        for city in obj_state.cities:
            list_cities.append(city.to_dict())
        return jsonify(list_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_object(city_id=None):
    """Retrieve one city based on city_id"""
    obj_city = storage.all(City)
    for key, value in obj_city.items():
        key_split = key.split(".")
        if city_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Delete one city based on city_id"""
    obj_city = storage.get(City, city_id)
    if obj_city:
        obj_city.delete()
        storage.save()
        return({})
    abort(404)
