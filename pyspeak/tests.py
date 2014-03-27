"""
.. module:: tests
   :synopsis: Unit tests for the pyspeak module.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import unittest
from collections import Iterable

from ahocorasick import KeywordTree

from common import (
    KeywordsNumberException, 
    MinKeywordLengthException, 
    UnknownLanguageException, 
)
from keywords import LangTree
from settings import LANG_CODES, KWORDS_MAX, MAX_WORD_LEN
from tweets import Tweet, TweetProvider


class TestTweet(unittest.TestCase):
    
    def setUp(self):
        self.text = "Testing this out."
        self.lang = 'en'
        self.tweet = Tweet(self.text, self.lang)
    
    def test_creation(self):
        self.assertRaises(UnknownLanguageException, Tweet, 
                          self.text, 'unknown')
        self.assertEqual(str(self.tweet), 
                         "(%s) %s" % (self.lang, self.text))
    
    def test_scores_initialized(self):
        init_scores = dict((lang, None) for lang in LANG_CODES)
        self.assertDictContainsSubset(init_scores, self.tweet.scores)


class TestTweetProvider(unittest.TestCase):
    
    def setUp(self):
        self.lang = 'en'
        self.provider = TweetProvider(self.lang)
    
    def test_creation(self):
        self.assertRaises(UnknownLanguageException, TweetProvider, 'unknown')
        self.assertIsInstance(self.provider, Iterable)
    
    def test_at_least_one_tweet(self):
        tweet = iter(self.provider).next()
        self.assertIsInstance(tweet, Tweet)


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
        self.assertIsInstance(self.lang_tree.tree, KeywordTree)
    
    def test_all_kwords_found(self):
        for kword in self.lang_tree.kwords:
            self.assertTrue(self.lang_tree.tree.search(kword))


if __name__ == "__main__":
    unittest.main()