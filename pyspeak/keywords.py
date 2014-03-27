"""
.. module:: keywords
   :synopsis: Helper class that deals with keyword extraction.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import ahocorasick

from common import (
    KeywordsNumberException, 
    MinKeywordLengthException, 
    UnknownLanguageException, 
)
from settings import ( 
    LANG_CODES, 
    KWORDS_PATH, 
    KWORDS_NAME, 
    KWORDS_MAX, 
    MAX_WORD_LEN, 
)


class LangTree(object):
    """
    A wrapper that loads up keywords for the given language into an 
    Aho-Corasick automaton, making them available for fast multiple 
    keyword/phrase search in texts/tweets. The keywords represent the top 100 
    most common words in a given language and are provided by the 
    http://wortschatz.uni-leipzig.de/ website. The keyword search uses the 
    ahocorasick library, available on PyPI.
    
    :param str lang: Language code for the most common words to load.
    :param kwords_cap: (Optional) maximum number of keywords to load.
    :param min_word_len: (Optional) keyword to have at least this many letters.
    :param KeywordTree tree: The suffix tree that is built and used for search.
    """
    
    def __init__(self, lang, kwords_cap=KWORDS_MAX, min_word_len=0):
        if lang not in LANG_CODES:
            raise UnknownLanguageException(lang)
        self.lang = lang
        
        if kwords_cap and 0 < kwords_cap <= KWORDS_MAX:
            self.n_kwords = kwords_cap
        else:
            raise KeywordsNumberException(kwords_cap)
        
        if 0 <= min_word_len <= MAX_WORD_LEN:
            self.min_word_len = min_word_len
        else:
            raise MinKeywordLengthException(min_word_len)
        
        self.tree = ahocorasick.KeywordTree()
        self.kwords = []
        with open(KWORDS_PATH + KWORDS_NAME.replace("(lang)", lang)) as f:
            for _ in xrange(self.n_kwords):
                kword = f.readline().strip()
                if len(kword) < self.min_word_len:
                    continue
                self.tree.add(kword)
                self.kwords.append(kword)
        
        self.tree.make()
    
    def __str__(self):
        return "(%s) LangTree" % self.lang
    
    def __repr__(self):
        return self.__str__()

