#!/usr/bin/python3
"""flask integration"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
# from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)
# swagger = Swagger(app)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})



@app.teardown_appcontext
def close(error):
    """Handles app teardown(close)"""
    storage.close()


@app.errorhandler(404)
def notfound(error):
    """Handles 404 errors in JSON format"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=int(port), threaded=True)
