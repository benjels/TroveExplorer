
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

class TroveArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
            #we need to build a list of dictionaries where each entry has a title and a url
            relatedArticles = []
            for eachTitle in troveArticle["relatedTopics"]:
                eachTitleURL = '{}/topic/{}'.format(APP_BASE_URL, eachTitle.replace(" ", "_"))
                relatedArticles.append({"title" : eachTitle, "topicURL" : eachTitleURL})
        troveArticle["relatedTopics"] = relatedArticles
        return troveArticle


class Topic(Resource):
    def get(self, title):
        with open(WIKIPEDIA_ARTICLES_PATH + title.replace(" ", "_") + ".json") as wikipediaJSON:
            #fill out a dictionary to return as json
            wikipediaJSONObj = json.load(wikipediaJSON)
            result = {}
            result['topicID'] = (wikipediaJSONObj['topicID'])
            result['title'] = (wikipediaJSONObj['title'])
            #now get the addtional info for each related trove article whose info we put under each trove entry
            relatedTroveArticlesInfo = []
            for eachTroveID in wikipediaJSONObj["relatedTroveArticles"]:
                troveArticle = TroveArticle().get(str(eachTroveID))
                troveArticle['troveURL'] = "{}/trove/{}".format(APP_BASE_URL, eachTroveID)
                relatedTroveArticlesInfo.append(troveArticle)#TODO: should just have a module level function that does this as a helper and is used by the two resource methods
            result['articles'] = relatedTroveArticlesInfo
            return result

class WikipediaArticleIntersection(Resource):
  def get(self, titles):
      listOfSearchTerms = titles.split("&")
      setsOfIDs = []
      for each in listOfSearchTerms:
        eachTopicRelatedArticles = Topic().get(each)["articles"]
        eachTopicRelatedArticlesIDs = set()
        for eachArticle in eachTopicRelatedArticles:
            eachTopicRelatedArticlesIDs.add(eachArticle["uid"])
        setsOfIDs.append(eachTopicRelatedArticlesIDs)
      #so now we have an array where each entry is a set of trove UIDs. We need to find their intersection
      result = {}
      intersectionIDs = set.intersection(*setsOfIDs)
      intersectionArticles = []
      for eachTroveID in intersectionIDs:
           troveArticle = TroveArticle().get(str(eachTroveID))
           troveArticle['troveURL'] = "{}/trove/{}".format(APP_BASE_URL, eachTroveID)
           intersectionArticles.append(troveArticle)
      result['articles'] = intersectionArticles
      #now we have the related trove articles, fill in the rest of the result
      result['searchedTopics'] = listOfSearchTerms #TODO: this should be a list of dictionaries where each entry has the title, id and a link to that topic's individual page
      return result






#TODO: consider removing this. just support verbose and trove
# class WikipediaArticle(Resource):
#     def get(self, wikipediaTitle):
#         filePath = "{}{}.json".format(WIKIPEDIA_ARTICLES_PATH, wikipediaTitle.replace(" ","_"))
#         with open(filePath, "r") as wikipediaFile:
#             wikipediaArticle = json.load(wikipediaFile)
#         return wikipediaArticle


api.add_resource(Home, '/')
api.add_resource(TroveArticle, '/trove/<troveID>')
api.add_resource(Topic, '/topic/<title>')
api.add_resource(WikipediaArticleIntersection, '/intersection/<titles>')
#api.add_resource(WikipediaArticle, '/wikipedia/<wikipediaTitle>')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=True)

   #print(WikipediaArticleIntersection().get("new zealand&auckland"))
