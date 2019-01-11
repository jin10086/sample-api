from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])
app.config.from_pyfile("config.py")
api = Api(app)
mongo = PyMongo(app)
cache = Cache(app, config={"CACHE_TYPE": "redis"})


class Api(Resource):

    def get(self, eos_account):
        data = mongo.db.accounts.find({"eos_account": eos_account}, {"_id": 0})
        return list(data)


api.add_resource(Api, "/<string:eos_account>")


if __name__ == "__main__":
    app.run(debug=False, port=5002, threaded=True)
