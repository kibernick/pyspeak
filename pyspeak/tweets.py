"""
.. module:: tweets
   :synopsis: Classes that import and wrap Twitter data.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

from settings import ( 
    LANG_CODES, 
    TWEETS_PATH, 
    TWEETS_NAME, 
)

class Tweet(object):
    """
    Holds the info on the tweet contect, it's original language and scores for
    each of the languages to predict.
    
    :param str text: Tweet text content.
    :param str lang_from: Language code of the tweet origin. Acceptable: ['de', 
    'en', 'fr', 'nl']
    :param dict scores: Scores for keywords in each language.
    """
    
    def __init__(self, text, lang_from):
        self.text = text
        if lang_from not in LANG_CODES:
            raise Exception("Language not recognized: " + str(lang_from))
        self.lang_from = lang_from
        self.scores = dict((lang, None) for lang in LANG_CODES)
    
    def __str__(self):
        return "(%s) %s" % (self.lang_from, self.text[:70])
    
    def __repr__(self):
        return self.__str__()
    
    def calc_score_for_lang(self, lang_tree):
        """
        Instance method to calculate the score for a given lang.
        
        :param LangTree lang_tree: Wrapper for ahocorasick with suffix tree.
        """
        score = len(lang_tree.tree.findall(self.text))
        self.scores[lang_tree.lang] = score


class TweetProvider(object):
    """
    An iterable that simulates a "stream" of tweets coming from a source. It
    loads tweets from predefined locations and provides a generator-like
    interface to retrieve them. Example of usage:
    
    >>> [tweet for tweet in TweetProvider('en')]
    
    >>> for tweet in TweetProvider('nl'):
            print tweet.scores
    
    :param str lang: Language code of the tweets to load.
    """
    
    def __init__(self, lang):
        if lang not in LANG_CODES:
            raise Exception("Language not recognized: " + str(lang))
        self.lang = lang
        with open(TWEETS_PATH + TWEETS_NAME.replace("(lang)", lang)) as f:
            self._tweets = [line.strip() for line in f.readlines()]
    
    def __iter__(self):
        for tweet in self._tweets:
            yield Tweet(tweet, self.lang)
    
    def __str__(self):
        return "TweetProvider (%s) (%s tweets)" % (self.lang,
                                                   str(len(self._tweets)))
