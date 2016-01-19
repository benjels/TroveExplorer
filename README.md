# TroveExplorer

Flask-Restful web app that lets users get information about Trove articles related to certain wikipedia articles.

The dependencies of this project are given in the requirement.txt file in this repo.

EXAMPLE USAGE(assuming you are hosting the app on localhost):

127.0.0.1/topic/north island&james cook

will return a JSON response that contains references and information about all of the Trove articles related to BOTH:
https://en.wikipedia.org/wiki/North_Island
AND
https://en.wikipedia.org/wiki/James_Cook

You can look at the information about individual trove articles by clicking the links to them in the returned JSON, or by searching something like this:

127.0.0.1/trove/<someTroveArticleID>

where <someTroveArticleID> is the unique ID of the Trove article that you want to find out about.




