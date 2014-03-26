"""
.. module:: main
   :synopsis: Rough language classification of tweets, using keyword matching.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import ahocorasick

from settings import ( 
    LANG_CODES, 
    KWORDS_PATH, 
    KWORDS_NAME, 
    KWORDS_MAX, 
)
from tweets import (
    Tweet, 
    TweetProvider, 
)
from keywords import 


def main():
    for lang in LANG_CODES:
        pass