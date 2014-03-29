import json
class InstagramMedia:
    """
        Wraps return from instagram api
        extracts desired items from instagra.media
        - caption_text = caption
        - comments = list of comments
        - date = posted date
        - tags = list of tags used
        - user = user who posted the photo
        - filter = filter used on photo
        - (future)
            likes = list of likes
            imgurls
    """
    def __init__(self, **kargs):
        self.date = kargs['date']
        self.mid = kargs['mid']
        self.tags = kargs['tags']
        self.like_count = kargs['like_count']
        self.comment_count = kargs['comment_count']
        self.caption = kargs['caption']
        self.comments = kargs['comments'],
        if (isinstance(self.comments, tuple)):
            try:
                self.comments = self.comments[0]
            except:
                print self.comments
        self.comment_users = kargs['comment_users']
        self.user = kargs['user']
        self.filter = kargs['filter']




    def json(self):
        results = self.__dict__
        if '_id' in results:
            del results['_id']
        return json.dumps(results)



def test():
    kargs = {
        "mid": "1234",
        "caption_text": "this is a caption",
        "comments": ["these", "are", "comments"],
        "date": "date",
        "tags": ["happy", "go", "lucky"],
        "user": "samuel",
        "filter": "valencia"
    }
    iM = InstagramMedia(**kargs)
    return iM

# iM = test()
