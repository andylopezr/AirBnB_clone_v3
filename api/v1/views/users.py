#!/usr/bin/python3
"""View fo User objects"""

from models import storage
from models.user import User
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """Retrieve all users based on state_id"""
    all_users = storage.all(User).values()
    return jsonify([obj.to_dict() for obj in all_users])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def one_user(user_id=None):
    """Retrieve a user based on user_id"""
    obj_user = storage.all(User)
    for key, value in obj_user.items():
        key_split = key.split(".")
        if user_id == key_split[1]:
            return jsonify(value.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Deletes user based on user_id"""
    obj_user = storage.get(User, user_id)
    if obj_user:
        key = 'User' + "." + obj_user.id
        obj_user.delete()
        storage.save()
        return({})
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """Creates a User based on json"""
    # transform the HTTP body request to a dictionary
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, 'Not a JSON')
    if "email" not in obj_dict:
        abort(400, 'Missing email')
    if "password" not in obj_dict:
        abort(400, 'Missing password')
    if 'name' in obj_dict.keys():
        obj_user = User(**obj_dict)
        obj_user.save()
        return jsonify(obj_user.to_dict()), 201
    else:
        abort(400, 'Missing name')


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates User based on user_id"""
    obj_user = storage.get(User, user_id)

    # These keys cannot be update
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    # transform the HTTP body request to a dictionary
    to_update = request.get_json()
    if to_update is None:
        abort(400, 'Not a JSON')
    # check if key in dictionary is not allowed to be updated
    for key_ignore in ignore_keys:
        if key_ignore in to_update.keys():
            del to_update[key_ignore]
    if obj_user:
        for key, value in to_update.items():
            setattr(obj_user, key, value)
        obj_user.save()
        return jsonify(obj_user.to_dict())
    else:
        abort(404)
