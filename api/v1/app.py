#!/usr/bin/python3
""" Status of your API """
from api.v1.views import app_views
from flask import Flask
from models import storage
import os
from flask import jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

#Edit this teardown
@app.teardown_appcontext
def teardown_appcontext(self):
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        host = '5000'
    app.run(host=host, port=port, threaded=True)
