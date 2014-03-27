"""
.. module:: main
   :synopsis: Rough language classification of tweets, using keyword matching.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import argparse

from settings import ( 
    LANG_CODES, 
    KWORDS_MAX, 
)
from tweets import TweetProvider
from keywords import LangTree


def initialize(kwords_cap=KWORDS_MAX, min_word_len=0):
    tweetsource, trees, tweets = {}, {}, []
    for lang in LANG_CODES:
        tweetsource[lang] = TweetProvider(lang)
        trees[lang] = LangTree(lang, kwords_cap, min_word_len)
        tweets.extend( list(tweetsource[lang]) )
    return trees, tweets


def get_tweets_and_infer_language(max_kwords=KWORDS_MAX, min_word_len=0):
    trees, tweets = initialize(kwords_cap=max_kwords, min_word_len=min_word_len)
    for tweet in tweets:
        for lang in LANG_CODES:
            lang_tree = trees[lang]
            tweet.calc_score_for_lang(lang_tree)
    
    for tweet in tweets:
        print tweet.detected, tweet


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rough language \
        classification of tweets, using keyword matching.')
    parser.add_argument('--max_kwords', nargs='?', type=int, 
                        help="maximum number of keywords to load")
    parser.add_argument('--min_kword_len', nargs='?', type=int, 
                        help="minimum keyword length to consider")
    args = parser.parse_args()
    
    max_kwords = args.max_kwords if args.max_kwords else KWORDS_MAX
    min_word_len = int(args.min_kword_len) if args.min_kword_len else 0
    
    get_tweets_and_infer_language(max_kwords, min_word_len)

