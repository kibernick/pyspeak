"""
.. module:: tests
   :synopsis: Unit tests for the pyspeak module.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import unittest
from collections import Iterable
import os

from ahocorasick import KeywordTree

from common import (
    KeywordsNumberException, 
    MinKeywordLengthException, 
    UnknownLanguageException, 
)
from keywords import LangTree
from main import initialize, infer_language
from settings import *
from tweets import Tweet, TweetProvider


class TestSettings(unittest.TestCase):
    
    def test_default_language(self):
        self.assertIn('en', LANG_CODES,
                      msg="English ('en') must be in testable languages.")
    
    def test_paths_exist(self):
        self.assertTrue(os.path.exists(TWEETS_PATH),
                        msg="Path 'TWEETS_PATH' does not exist.")
        self.assertTrue(os.path.exists(KWORDS_PATH),
                        msg="Path 'KWORDS_PATH' does not exist.")
    
    def test_input_files_available(self):
        for lang in LANG_CODES:
            tweetpath = (TWEETS_PATH + TWEETS_NAME).replace("(lang)", lang)
            self.assertTrue(os.path.isfile(tweetpath), 
                            msg="Missing tweets file.")
            kwordspath = (KWORDS_PATH + KWORDS_NAME).replace("(lang)", lang)
            self.assertTrue(os.path.isfile(kwordspath), 
                            msg="Missing keywords file.")


class TestTweet(unittest.TestCase):
    
    def setUp(self):
        self.text = "Testing tweets."
        self.lang = 'en'
        self.tweet = Tweet(self.text, self.lang)
    
    def test_creation(self):
        self.assertRaises(UnknownLanguageException, Tweet, 
                          self.text, 'unknown')
        self.assertEqual(str(self.tweet), 
                         "(%s) %s" % (self.lang, self.text[:70]),
                         msg="Incorrect string representation of Tweet.")
    
    def test_scores_initialized(self):
        init_scores = dict((lang, None) for lang in LANG_CODES)
        self.assertDictContainsSubset(init_scores, self.tweet.scores,
                                      msg="Scores not initialized.")


class TestTweetProvider(unittest.TestCase):
    
    def setUp(self):
        self.lang = 'en'
        self.provider = TweetProvider(self.lang)
    
    def test_creation(self):
        self.assertRaises(UnknownLanguageException, TweetProvider, 'unknown')
        self.assertIsInstance(self.provider, Iterable,
                              msg="TweetProvider should be Iterable.")
    
    def test_at_least_one_tweet(self):
        tweet = iter(self.provider).next()
        self.assertIsInstance(tweet, Tweet,
                              msg="Could not retrieve at least one Tweet.")


class TestLangTree(unittest.TestCase):
    
    def setUp(self):
        self.lang = 'en'
        self.lang_tree = LangTree(self.lang)
    
    def test_creation(self):
        invalid_caps = 0, KWORDS_MAX + 1
        invalid_lens = -1, MAX_WORD_LEN + 1
        self.assertRaises(KeywordsNumberException, LangTree, 
                          self.lang, kwords_cap=invalid_caps[0])
        self.assertRaises(KeywordsNumberException, LangTree, 
                          self.lang, kwords_cap=invalid_caps[1])
        self.assertRaises(MinKeywordLengthException, LangTree, 
                          self.lang, min_word_len=invalid_lens[0])
        self.assertRaises(MinKeywordLengthException, LangTree, 
                          self.lang, min_word_len=invalid_lens[1])
        self.assertIsInstance(self.lang_tree.tree, KeywordTree,
                              msg="Suffix tree not initialized correctly.")
    
    def test_all_kwords_found(self):
        for kword in self.lang_tree.kwords:
            self.assertTrue(self.lang_tree.tree.search(kword),
                            msg="Could not find keyword in tree!")


class TestLanguageInference(unittest.TestCase):
    
    def setUp(self):
        self.trees, self.tweets = initialize()
        infer_language(self.trees, self.tweets)
    
    def test_tweet_scores_calculated(self):
        at_least_one = False
        for tweet in self.tweets:
            if tweet.detected != "??":
                self.assertIn(tweet.detected, LANG_CODES,
                              msg="Inferred an unknown language.")
                at_least_one = True
        self.assertTrue(at_least_one,
                        msg="Not a single language was infered.")


if __name__ == "__main__":
    unittest.main()