
from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

TROVE_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\TroveJSON\\"
WIKIPEDIA_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\WikipediaJSON\\"


class Home(Resource):
    def get(self):
        return {
            'hello': 'world',
        }

class TroveArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
        return troveArticle

class WikipediaArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
        return troveArticle


api.add_resource(Home, '/')
api.add_resource(TroveArticle, '/trove/<troveID>')
api.add_resource(WikipediaArticle, '/wikipedia/<wikipediaTitle>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=False)