import twint
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json
import os

app = Flask(__name__)
api = Api(app)


class Twint_tweet(Resource):

    def post(self, target, search):

        # Configure
        with open("results.json", "w"):
            pass

        c = twint.Config()
        c.Username = target
        if search.strip():
            c.Search = search

        c.Output = "results.json"
        c.Store_json = True
        c.Format = "Tweet id: {id} | Tweet: {tweet}"

        # Run
        twint.run.Search(c)
        return "ok", 201

    def get(self, target, search):
        with open('results.json') as f:
            table = f.readlines()
            data = {"target": target, "search": search, "data": table}
            return data, 200

class Twint_relation(Resource):
    def post(self, target):
        c = twint.Config()
        c.Username = target
        c.Output = "relation.txt"
        #c.Store_json = True
        twint.run.Followers(c)
        return "ok", 201

    def get(self, target):
        with open('relation.json') as f:
            table = f.readlines()
            data = {"target": target, "folowers": table}

            return data, 200


api.add_resource(Twint_tweet, "/twint_tweet/<string:target>/<string:search>")
api.add_resource(Twint_relation, "/twint_relation/<string:target>")
app.run(debug=True, port=5014, threaded=True)



'''c = twint.Config()
c.Username = "fiacresoubgui"
c.Search = "osint"
c.Output = "results.csv"
c.Store_csv = True
twint.run.Search(c)'''
