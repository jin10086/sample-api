from __future__ import absolute_import, unicode_literals

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_redis import FlaskRedis

from ut import check

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])
app.config.from_pyfile("config.py")
api = Api(app)
mongo = PyMongo(app)
redis_store = FlaskRedis(app)


class Api(Resource):

    def get(self, address):
        if redis_store.get(address):
            return {"status": 0, "msg": "请不要点击太快."}
        redis_store.set(address, 1, 10)
        return check(address)


api.add_resource(Api, "/<string:address>")


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
