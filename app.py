from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:8080","http://boslaoge.me","https://boslaoge.me"])
app.config.from_pyfile("config.py")
api = Api(app)
mongo = PyMongo(app)
cache = Cache(app, config={"CACHE_TYPE": "redis"})


class Api(Resource):

    def get(self):
        return {"hello": "world"}


api.add_resource(Api, "/")


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
