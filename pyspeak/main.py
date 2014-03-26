"""
.. module:: main
   :synopsis: Rough language classification of tweets, using keyword matching.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import ahocorasick

from settings import ( 
    LANG_CODES, 
    TWEETS_PATH, 
    TWEETS_NAME, 
    KWORDS_PATH, 
    KWORDS_NAME, 
)
from tweets import (
    Tweet, 
    TweetProvider, 
)


