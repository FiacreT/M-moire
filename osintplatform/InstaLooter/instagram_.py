
from instalooter.looters import ProfileLooter
from instalooter.looters import HashtagLooter

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
users = set()
users_comment = set()

def links(media, looter):
    if media.get('__typename') == "GraphSidecar":
        media = looter.get_post_info(media['shortcode'])
        nodes = [e['node'] for e in media['edge_sidecar_to_children']['edges']]
        return [n.get('video_url') or n.get('display_url') for n in nodes]
    elif media['is_video']:
        media = looter.get_post_info(media['shortcode'])
        return [media['video_url']]
    else:
        return [media['display_url']]

class Instalooter_download_image(Resource):
    def post(self, target, number_media):
        looter = ProfileLooter(target)
        looter.download('Pictures/'+target, media_count=int(number_media))
        return "ok", 201

class Instalooter_download_hashtag(Resource):
    def post(self, hashtag_):
        looter = HashtagLooter("hashtag_")

        with open("hashtag/"+hashtag_+".txt", "w") as f:
            for media in looter.medias():
                for link in links(media, looter):
                    f.write("{}\n".format(link))
        return "ok", 201
    
    def get(self, hashtag_):
        with open("hashtag/"+hashtag_+".txt") as f:
            result = f.readlines()
        
        results = {
            "hashtag" : hashtag_,
            "link" : result
        }
        return results, 200


class Instalooter_download_user_mention(Resource):
    def post(self, target):
        looter = ProfileLooter(target)
        
        for media in looter.medias():
            post_info = looter.get_post_info(media['shortcode'])
            for comment in post_info['edge_media_to_tagged_user']['edges']:
                user = comment['node']['user']['username']
                users.add(user)
        return "ok", 201

    def get(self, target):
        results = {
            "target": target,
            "mention": list(users)
        }
        return results, 200


class Instalooter_who_comment(Resource):
    def post(self, target):
        looter = ProfileLooter(target)

        for media in looter.medias():
            post_info = looter.get_post_info(media['shortcode'])
            for comment in post_info['edge_media_to_comment']['edges']:
                user = comment['node']['owner']['username']
                users_comment.add(user)
            return "ok", 201
    
    def get(self, target):
        results = {
            "target": target,
            "who_comment": list(users_comment)
        }
        return results, 200

api.add_resource(Instalooter_download_image, "/instalooter_download_image/<string:target>/<string:number_media>")
api.add_resource(Instalooter_download_hashtag, "/instalooter_download_hashtag/<string:hashtag_>")
api.add_resource(Instalooter_download_user_mention, "/instalooter_download_mention/<string:target>")
api.add_resource(Instalooter_who_comment, "/instalooter_who_comment/<string:target>")
app.run(debug=True, port=5011, threaded=True)