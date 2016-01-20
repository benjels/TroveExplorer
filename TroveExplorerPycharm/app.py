
from flask import Flask
from flask import render_template
from flask_restful import Resource, Api
import json

app = Flask(__name__)

@app.route("/")
def home():
    return("there's nobody here")

#TODO: It is a good idea to do as much processing in here rather than in the jinja template right?
@app.route('/topic/<title>')
def queryTopics(title):
    return render_template('topic.html', topics = Topic().get(title)["searchedTopics"], troves = Topic().get(title)["articles"])

@app.route('/trove/<troveID>')
def queryTrove(troveID):
    return render_template('trove.html', articleTitle = TroveArticle().get(troveID)["title"], relatedTopics = TroveArticle().get(troveID)["relatedTopics"], fulltext = TroveArticle().get(troveID)["fulltext"])


########################################## API ###############################################################



TROVE_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\TroveJSON\\"
WIKIPEDIA_ARTICLES_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\WikipediaJSON\\"
VERBOSE_WIKIPEDIA_PATH = "C:\\!2015SCHOLARSHIPSTUFF\\verboseJSON\\"
#API_BASE_URL = "http://bengelkite.pagekite.me//api"
API_BASE_URL = "http://127.0.0.1/api"


class TroveArticle(Resource):
    def get(self, troveID):
        filePath = "{}{}.json".format(TROVE_ARTICLES_PATH, troveID)
        with open(filePath, "r") as troveFile:
            troveArticle = json.load(troveFile)
            #we need to build a list of dictionaries where each entry has a title and a url
            relatedTopics = []
            for eachTitle in troveArticle["relatedTopics"]:
                eachTitleURL = '{}/topic/{}'.format(API_BASE_URL, eachTitle.replace(" ", "_"))
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
        searchedTopics.append({"title" : eachTopicJSON["title"], "topicID" : eachTopicJSON["topicID"], "URL" : "{}/topic/{}".format(API_BASE_URL, eachTopicJSON["title"].replace(" ", "_"))})
        setsOfIDs.append(set(eachTopicJSON["relatedTroveArticles"]))
      result["searchedTopics"] = searchedTopics
      #so now we have an array where each entry is a set of trove UIDs. We need to find their intersection and then make JSON dictionaries for each trove article of interest.
      intersectionIDs = set.intersection(*setsOfIDs)
      intersectionArticles = []
      for eachTroveID in intersectionIDs:
           troveArticle = TroveArticle().get(str(eachTroveID))
           troveArticle['troveURL'] = "{}/trove/{}".format(API_BASE_URL, eachTroveID)
           intersectionArticles.append(troveArticle)
      result['articles'] = intersectionArticles
      return result


api = Api(app)
api.add_resource(TroveArticle, '/api/trove/<troveID>')
api.add_resource(Topic, '/api/topic/<titles>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("80"), debug=True)

