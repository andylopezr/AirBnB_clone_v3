#!/usr/bin/python3
"""
It´s time to start the API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns a JSON from API route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
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

    stat = {name:  storage.count(obj) for obj, name in stats.items()}
    return jsonify(stat)
