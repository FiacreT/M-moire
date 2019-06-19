#!/usr/bin/env python3
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse
import darksearch

app = Flask(__name__)
api = Api(app)


class Darksearch(Resource):
    def post(self, target, n):
        client = darksearch.Client(timeout=30, headers=None, proxies=None)
        results = client.search(target, page=int(n))
        return results, 201






api.add_resource(Darksearch, "/darksearch/<string:target>/<string:n>")
app.run(debug=True)