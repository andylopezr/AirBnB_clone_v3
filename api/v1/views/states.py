#!/usr/bin/python3

from models import storage
from models.state import State
from flask import Flask, jsonify
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
    return jsonify({"error": "Not found"}), 404


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
    return jsonify({"error": "Not found"}), 404
