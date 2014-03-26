"""
.. module:: keywords
   :synopsis: Helper class that deals with keyword extraction.

.. moduleauthor:: Nikola Rankovic <kibernick@gmail.com>
"""

import ahocorasick

from settings import ( 
    LANG_CODES, 
    KWORDS_PATH, 
    KWORDS_NAME, 
    KWORDS_MAX, 
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
    :param KeywordTree tree: The suffix tree that is built and used for search.
    """
    
    def __init__(self, lang, kwords_cap=KWORDS_MAX):
        if lang not in LANG_CODES:
            raise Exception("Language not recognized: " + str(lang))
        self.lang = lang
        if kwords_cap and 0 < kwords_cap <= KWORDS_MAX:
            self.n_kwords = kwords_cap
        else:
            raise Exception("Invalid number of keywords to import: " + str(kwords_cap))
        self.tree = ahocorasick.KeywordTree()
        
        with open(KWORDS_PATH + KWORDS_NAME.replace("(lang)", lang)) as f:
            for _ in xrange(self.n_kwords):
                kword = f.readline().strip()
                self.tree.add(kword)
        
        self.tree.make()
    
    def __str__(self):
        return "(%s) LangTree" % self.lang
    
    def __repr__(self):
        return self.__str__()

