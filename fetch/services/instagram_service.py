from instagram.client import InstagramAPI
import twitter_sentiment.models.InstagramMedia as InstagramMedia
# move this to settings in cleanup
ACCESS_TOKEN = '194916491.e8bddc5.f6a363bb1db74f808cf0e55c6dca9e53'


class InstagramService:

    """
        Wrap access to Instagram API in a service
    """

    def __init__(self, access_token, pages=1):
        self.api = InstagramAPI(access_token=access_token)
        self.pages = pages
        self.api_calls = 0
        self.results_found = 0

    def search(self, tag_name, count=30):
        """
            Searches instagram api for tag_name and returns recent media
        """
        callback_offset = -13  # hackey way to find lastid
        tag_recent_media = {}
        max_id = None
        for page in range(self.pages):
            print "searching for {0} with id {1} on loop {2}".format(tag_name, max_id, page)
            media, callback = self.api.tag_recent_media(
                count=count, tag_name=tag_name, max_tag_id=max_id)
            self.api_calls += 1
            # collect media
            for each in media:
                if each.id in tag_recent_media:
                    print each.id + " already exists..."
                tag_recent_media[each.id] = self.wrap_media(each)
            max_id = callback[callback_offset:]
        self.results_found += len(tag_recent_media)
        return tag_recent_media

    def wrap_media(self, media):
        comments = []
        for comment in media.comments:
            """try:
                text = comment.text.encode("utf-8")
            except:
                text = ''"""
            comments.append(comment.text)
        # we need text cleaning
        config = {
            'mid': media.id,
            'user': media.user.username,
            'date': media.created_time.strftime("%y-%m-%d-%h-%M-%S"),
            'tags': [tag.name for tag in media.tags],
            'like_count': media.like_count,
            'comment_count': media.comment_count,
            'caption': media.caption.text if media.caption else '',
            'comments': comments,
            'comment_users': [comment.user.username for comment in media.comments],
            'filter': media.filter
        }
        instagramMedia = InstagramMedia.InstagramMedia(**config)

        #print instagramMedia.comments
        return instagramMedia



def test_search():
    pass



# i = InstagramService(ACCESS_TOKEN)
# v = i.search("Ukrain")
# s = v.values()[0]
