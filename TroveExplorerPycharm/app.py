#TODO:UNRELATED TO THIS PROGRAM check encoding that I am using to write to files in java... (some characters are being lost) e.g. Maori a grave/acute symbol thins was getting lost in my google docs dump
from flask import Flask
from flask_restful import Resource, Api
import json



TROVE_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\TroveJSON\\"
WIKIPEDIA_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\WikipediaJSON\\"
VERBOSE_WIKIPEDIA_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\verboseJSON\\"
#APP_BASE_URL = "http://bengelkite.pagekite.me"
APP_BASE_URL = "http://127.0.0.1"



class Home(Resource):
    def get(self):
        return {
            'search for all trove articles related to a wikipedia title and display their IDs': 'http://127.0.0.1/topic/<some title here>',
            'search for a particular trove article and display the titles of related wikipedia articles': 'http://127.0.0.1/trove/<some trove ID here>'
        }


class TroveArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
            #we need to build a list of dictionaries where each entry has a title and a url
            relatedTopics = []
            for eachTitle in troveArticle["relatedTopics"]:
                eachTitleURL = '{}/topic/{}'.format(APP_BASE_URL, eachTitle.replace(" ", "_"))
                relatedTopics.append({"title" : eachTitle, "topicURL" : eachTitleURL})
        troveArticle["relatedTopics"] = relatedTopics
        return troveArticle


class Topic(Resource):
  def get(self, titles):
      result = {}
      setsOfIDs = []
      searchedTopics = []
      listOfSearchTerms = titles.split("&")
      #for each of the topics that the user has queried, go and get the info for that topic. Including the trove articles it is related to so that we can use them to find the intersection.
      for eachTerm in listOfSearchTerms:
        with open("{}{}.json".format(WIKIPEDIA_ARTICLES_PATH, eachTerm.replace(" ", "_"))) as eachTopicJSONFile:
            eachTopicJSON = json.load(eachTopicJSONFile)
        searchedTopics.append({"title" : eachTopicJSON["title"], "topicID" : eachTopicJSON["topicID"], "URL" : "{}/topic/{}".format(APP_BASE_URL, eachTopicJSON["title"].replace(" ", "_"))})
        setsOfIDs.append(set(eachTopicJSON["relatedTroveArticles"]))
      result["searchedTopics"] = searchedTopics
      #so now we have an array where each entry is a set of trove UIDs. We need to find their intersection and then make JSON dictionaries for each trove article of interest.
      intersectionIDs = set.intersection(*setsOfIDs)
      intersectionArticles = []
      for eachTroveID in intersectionIDs:
           troveArticle = TroveArticle().get(str(eachTroveID))
           troveArticle['troveURL'] = "{}/trove/{}".format(APP_BASE_URL, eachTroveID)
           intersectionArticles.append(troveArticle)
      result['articles'] = intersectionArticles
      return result


app = Flask(__name__)
api = Api(app)
api.add_resource(Home, '/')
api.add_resource(TroveArticle, '/trove/<troveID>')
api.add_resource(Topic, '/topic/<titles>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=True)

