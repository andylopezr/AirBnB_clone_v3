#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Returns a JSON from API route"""
    return jsonify({"status": "OK"})
