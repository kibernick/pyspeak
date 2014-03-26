"""
.. module:: main
   :synopsis: Rough language classification of tweets, using keyword matching.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

from settings import ( 
    LANG_CODES, 
)
from tweets import TweetProvider
from keywords import LangTree


def initialize():
    tweetsource, trees, tweets = {}, {}, []
    for lang in LANG_CODES:
        tweetsource[lang], trees[lang] = TweetProvider(lang), LangTree(lang)
        tweets.extend( list(tweetsource[lang]) )
    return trees, tweets


def main():
    trees, tweets = initialize()
    for tweet in tweets:
        for lang in LANG_CODES:
            lang_tree = trees[lang]
            tweet.calc_score_for_lang(lang_tree)
    
    for tweet in tweets:
        print tweet.detected, tweet
    


if __name__ == "__main__":
    main()