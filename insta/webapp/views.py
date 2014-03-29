from app import app
from flask import render_template, request, jsonify
import twitter_sentiment.fetch.services.instagram_service as instagram_service
import db
import settings
import json
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch/<tag>")
def fetch_tag(tag):
    iService = instagram_service.InstagramService(settings.access_token)

    results = iService.search(tag)
    print "Tag = {0} results = {1}".format(tag, len(results))
    json_results = {}
    mdb = db.MongoDBService()
    for mid, i_media in results.iteritems():
        print mdb.exists('mid', mid).count()
        if mdb.exists('mid', mid).count():
            print "skipping {0}".format(mid)
        else:
            print "inserting {0}".format(mid)

            mdb.insert(i_media.__dict__)
        json_results[mid] = i_media.json()



    
    return jsonify(json_results)

"""mSummary = media_summary.MediaSummary(**{'media_index': results})
tFreq = mSummary.tag_frequency()
fFreq = mSummary.filter_frequency()
capKeywords = mSummary.caption_keywords()
comKeywords = mSummary.comment_keywords()
like_stats = mSummary.like_stats()
print tFreq
print fFreq
print capKeywords
print comKeywords
print like_stats"""
