from instagram.client import InstagramAPI

from pattern.vector import count as vec_count
import icode.settings as settings
import sys
import re
CLIENT_SECRET = '04e72f5e767147bbb4da6168c3495270'
CLIENT_ID = 'e8bddc5ef0e5460cbc5c05a8945c282f'
REDIRECT_URL = 'http://127.0.0.1:5000/login'
ACCESS_TOKEN = '194916491.e8bddc5.f6a363bb1db74f808cf0e55c6dca9e53'
USER_ID = '194916491'
api = InstagramAPI(access_token=settings.ACCESS_TOKEN)

# api = InstagramAPI(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
class InstagramSearch:
    def __init__(self):
        self.api = InstagramAPI(access_token=settings.ACCESS_TOKEN)
        self.api_calls = 0

    def tag_recent_media(self, tag_name, count=100):
        """
            Searches instagram api for tag_name and returns recent media
        """
        tag_recent_media = {}
        max_id = None
        for pg in range(settings.PAGES):
            print "searching for {0} with id {1} on loop {2}".format(tag_name,max_id,pg)
            media, callback = self.api.tag_recent_media(count=count, tag_name=tag_name, max_tag_id = max_id)
            self.api_calls+=1
          #  return media,callback
            for each in media:
                if each.id in tag_recent_media:
                    print each.id + " already exists..."
                tag_recent_media[each.id] = each

            max_id = callback[-13:]
            
        return tag_recent_media


if __name__ == '__main__':
    # example search
    iS = InstagramSearch()
    trm = iS.tag_recent_media("snowy")