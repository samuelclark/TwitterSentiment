import pattern.web as patweb
# fix auth bug
patweb.TWITTER = "https://api.twitter.com/1.1/"
class TwitterService:
    """
        Wrap access to Twitter in a service -- more methods to add
    """ 
    def __init__(self):
        self.language = 'en'

    def trends(self):
        """
            returns trends
        """
        twitter = patweb.Twitter(language='en')
        return twitter.trends(cached=False)

    def search(self, term, pages=10, count=100):
        """
            searches twitter for <term>
            returns pages * count tweets in an {id: tweet}
        """
        tweets = {}
        twitter = patweb.Twitter(language=self.language)
        id = None
        for page in range(pages):
            for tweet in twitter.search(term, start=id, count=count):
                tweets[tweet.id] = tweet
                id = tweet.id
            print "term = {0} page = {1} collected = {2}".format(
                term.encode('ascii', 'ignore'),
                page, len(tweets))
        return tweets


def test_search():
    term = 'Ukraine'
    ts= TwitterService()
    try:
        result = ts.search(term, 1, 100)
    except Exception as e:
        print e
        result = []
    return result

test = True
if test:
    val = test_search()