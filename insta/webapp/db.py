from app import app, mongo

class MongoDBService:
    """
        An interface to apps mongo instance
    """
    def __init__(self):
        """
            db = name of mongo collection
        """
        with app.app_context():
            self.db = mongo.db.twitter

    def insert(self, info):
        """
            need some type of validation on info to keep table clean
        """
        assert isinstance(info, dict), "info must be a dict"

        success = False
        with app.app_context():
            try:
                self.db.insert(info)
                success = True
                #mongo.db.twitter.insert(info)
            except Exception as e:
                print e
        return success

    def exists(self, key, val):
        """
            searches db for key-val pair
            example:  
                key ='id', val = 10
        """
        #return mongo.db.twitter.find({key: val})
        with app.app_context():
            res = self.db.find({key: val})
            print res
            return res

    def remove(self, key, val):
        """
            removes key-val pair from db
            example:  
                key ='id', val = 10
        """
        #mongo.db.twitter.remove({'search_term': trend})
        success = False
        try:
            with app.app_context():
                success = True
                return self.db.remove({key: val})
        except Exception as e:
            print e
        return success


def test_mongo():
    test_info = {"text": "Ukraine is tense", "tid": "125", "name": "sam", 'keywords': ["sam", "is", "hungry"]}
    mdb = MongoDBService()
    k = 'tid'
    v = '124'
    print "inserting {0}".format("info")
    mdb.insert(test_info)
    print "looking up {0}/{1}".format(k, v)
    return mdb.exists(k, v)
    # print "removing {0}/{1}".format(k, v)
    # print mdb.remove(k, v)


# test_mongo()