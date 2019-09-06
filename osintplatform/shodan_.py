import shodan
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

SHODAN_API_KEY = "7UaqyjHPALsDbKlnxIQN4XasNe55Rr8i"

api_ = shodan.Shodan(SHODAN_API_KEY)
result_shodan = []

class Shodan_(Resource):
    def post(self, target):
        # Wrap the request in a try/ except block to catch errors
        try:
            # Search Shodan
            results = api_.search(target)
            # Show the results
            print('Results found: {}'.format(results['total']))
            print(results)
            for result in results['matches']:
                '''print('IP: {}'.format(result['ip_str']))
                print(result['data'])
                print('')'''
                data = {"IP":result['ip_str'], "description": result['isp'], "location": result['location'], "data":result['data']}
                result_shodan.append(data)
            print("-----------------------------------------------------------------------------------------")
            print(result_shodan)
        except shodan.APIError as e:
            print('Error: {}'.format(e))
        
        return {"target": target, "data": result_shodan}, 201


api.add_resource(Shodan_, "/shodan/<string:target>")
app.run(debug=True, port=5017, threaded=True)