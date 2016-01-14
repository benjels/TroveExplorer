
from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

TROVE_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\TroveJSON\\"
WIKIPEDIA_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\WikipediaJSON\\"
VERBOSE_WIKIPEDIA_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\verboseJSON\\"
APP_BASE_URL = "http://bengelkite.pagekite.me"


class Home(Resource):
    def get(self):
        return {
            'search for all trove articles related to a wikipedia title and display their content': 'http://127.0.0.1/verbose/<some title here>',
            'search for all trove articles related to a wikipedia title and display their IDs': 'http://127.0.0.1/wikipedia/<some title here>',
            'search for a particular trove article and display the titles of related wikipedia articles': 'http://127.0.0.1/trove/<some trove ID here>'
        }
#TODO: check encoding that I am using to write to files in java... (some characters are being lost) e.g. Maori
#todo: get this to return links to related wikiopedia articles
class TroveArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
            troveArticle['url'] = '{}{}'.format(APP_BASE_URL, troveArticle['uid'])
        return troveArticle


class WikipediaArticle(Resource):
    def get(self, wikipediaTitle):
        filePath = "{}{}.json".format(WIKIPEDIA_ARTICLES_PATH, wikipediaTitle.replace(" ","_"))
        with open(filePath, "r") as wikipediaFile:
            wikipediaArticle = json.load(wikipediaFile)
        return wikipediaArticle


class WikipediaArticleVerbose(Resource):
    def get(self, title):
        with open(WIKIPEDIA_ARTICLES_PATH + title.replace(" ", "_") + ".json") as wikipediaJSON:
            #fill out a dictionary to return as json
            wikipediaJSONObj = json.load(wikipediaJSON)
            result = {}
            result['topicID'] = (wikipediaJSONObj['topicID'])
            result['title'] = (wikipediaJSONObj['title'])
            #now get the addtional info for each related trove article
            relatedTroveArticlesInfo = []
            for eachTroveID in wikipediaJSONObj["relatedTroveArticles"]:
                troveArticle = TroveArticle().get(str(eachTroveID))
                troveArticle["fulltext"] = "" #TODO: get rid of this
                troveArticle['troveURL'] = "{}/trove/{}".format(APP_BASE_URL, eachTroveID)
                relatedTroveArticlesInfo.append(troveArticle)#TODO: should just have a module level function that does this as a helper and is used by the two resource methods
            result['articles'] = (relatedTroveArticlesInfo)
            return result

 # class WikipediaArticleIntersection(Resource):
 #     def get(self, titles):
 #         listOfSearchTerms = titles.split("&")
 #         setsOfIDs = set() #each article has a set of IDs and we want their intersection
 #         for each in listOfSearchTerms:
 #             articleJSON = json.loads(WikipediaArticle().get(each))
 #             print(articleJSON)






api.add_resource(Home, '/')
api.add_resource(TroveArticle, '/trove/<troveID>')
api.add_resource(WikipediaArticle, '/wikipedia/<wikipediaTitle>')
api.add_resource(WikipediaArticleVerbose, '/verbose/<title>')
# api.add_resource(WikipediaArticleIntersection, '/intersection/<titles>')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=True)
   # WikipediaArticleIntersection().get("new zealand&auckland")
