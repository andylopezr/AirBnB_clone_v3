#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON from API route"""
    return jsonify({"status": "OK"})


@app_views.route('/status')
def stats():
    """Returns number of objects by type"""
    stats = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for obj, name in stats.items()
    return jsonify({name: storage.count(obj)})
