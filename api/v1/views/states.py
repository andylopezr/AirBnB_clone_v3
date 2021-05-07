#!/usr/bin/python3
"""View for State objects"""

from models import storage
from models.state import State
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views

state = 'State'


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieve an object into a valid JSON"""
    all_states = storage.all(state).values()
    return jsonify([obj.to_dict() for obj in all_states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id=None):
    """Retrieve an object based on state_id"""
    state_obj = storage.all(state)
    for key, value in state_obj.items():
        key_split = key.split(".")
        if state_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_states(state_id):
    """Delete state based on state_id"""
    obj_state = storage.get(State, state_id)
    if obj_state:
        key = 'State' + "." + obj_state.id
        obj_state.delete()
        storage.save()
        return({})
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def post_states():
    """Post state based on json"""
    # transform the HTTP body request to a dictionary
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if 'name' in obj_dict.keys():
        obj_state = State(**obj_dict)
        obj_state.save()
        return jsonify(obj_state.to_dict()), 201
    else:
        abort(400, 'Missing name')


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_states(state_id):
    """Update state based on state_id"""
    obj_state = storage.get(State, state_id)

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
    if obj_state:
        for key, value in to_update.items():
            setattr(obj_state, key, value)
        obj_state.save()
        return jsonify(obj_state.to_dict())
    else:
        abort(404)
