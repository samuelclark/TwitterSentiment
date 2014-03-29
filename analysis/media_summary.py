import pattern.vector as patvec
class MediaSummary:
    def __init__(self, **kargs):
        self.media_index = kargs['media_index']

    def tag_frequency(self):
        tag_frequency = {}
        for mid, media in self.media_index.iteritems():
            tags = media.tags
            for tag in tags:
                tag_frequency[tag] = tag_frequency.get(tag, 0) + 1

        return tag_frequency

    def keywords(self, text, top=10):
        """
            Create pattern.vector.Document from text 
            Return keywords[:top]
        """

        doc = self.get_document(text)
        return doc.keywords(top=top)


    def get_document(self, text, stopwords=False):
        """
            turns text into pattern.vector Document
        """
        if stopwords:
            stopwords = patvec.stopwords
        return patvec.Document(text, stopwords=stopwords)

    def caption_keywords(self, top=10):
        """
            Aggregate caption text, generate keywords
            return caption_keywords[:top]
        """
        caption_text = " ".join([media.caption for mid, media in self.media_index.iteritems()])
        return self.keywords(caption_text)

    def comment_keywords(self, top=10):
        """
            Aggregate comment text, generate keywords
            return comment_keywords[:top]
        """
        comment_text = " ".join([comment for mid, media in self.media_index.iteritems() for comment in media.comments])
        return self.keywords(comment_text)

    def filter_frequency(self):
        """
            Calculates filter frequency distribution and returns it
        """
        filter_frequency = {}
        for mid, media in self.media_index.iteritems():
            filter_frequency[media.filter] = filter_frequency.get(media.filter, 0) + 1
        return filter_frequency

    def like_stats(self):
        """
            Returns the total number of likes for a set of instagram media
        """
        likes = [media.like_count for mid, media in self.media_index.iteritems()]
        total_likes = sum(likes)
        min_likes = min(likes)
        max_likes = max(likes)
        avg_likes = float(total_likes) / len(likes)
        return {
            'total': total_likes,
            'min': min_likes,
            'max': max_likes,
            'avg': avg_likes
            }


    # tag
    # rate
    # num instagrams
    # caption keywords
    # comment keywords
    # tag distribution
    # mentions
    # sentiment
    # filters
    # like totals

