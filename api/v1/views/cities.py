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
