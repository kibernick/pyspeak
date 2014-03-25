pyspeak
=======

The aim is to do rough language classification of a continuous stream of documents, using keyword matching.

The program is given a set of languages, and for each language a list of keywords. The program will say for each document, in which language is its text (or "I don't know"), based on whether it finds any keywords it knows. The idea is to be able to have many rules like this "If the text contains rijkswaterstaat it's in dutch", "If it contains Deutsche it's in german" etc.

Input data
----------

Keywords obtrainted from University of Leipzig Frequency Lists:

http://wortschatz.uni-leipzig.de/Papers/top100nl.txt
http://wortschatz.uni-leipzig.de/Papers/top100en.txt
http://wortschatz.uni-leipzig.de/Papers/top100de.txt
http://wortschatz.uni-leipzig.de/Papers/top100fr.txt

Tweets obtained from https://twitter.com/search, under search terms "lang:nl", "lang:en", etc. Selected first 20 tweets in each language, so that we "know" they are in that language (vague tweets like "OK" ignored for now, may be used for testing and experiments later). For now assume short documents, so just analysing the whole "document" (or tweet in this case) is fine.

Solution
--------

Each document would have a "score" for each language we are looking up. This score could be just a counter of how many keywords were found in a document, or perhaps something that also takes into account that a word was found in language A but not in language B, etc.

Makes use of the library that implements a fast multiple keyword/phrase search in texts (e.g. Aho–Corasick string matching algorithm - https://pypi.python.org/pypi/ahocorasick/0.9) and runs these for each incoming document per keyword set, and get scores that way.

Solution implemented as a single-run script for now.

The output could be a list of matching languages, sorted by score. Depending on implementation, could also be returned as JSON.

If testing out different configurations of the solution, we could also return the time it took to calculate the results.

Disregarding the case where there are multiple languages in one sentence. One classification result per input-text is enough. If the program can not analyse the input data for some reason, it should return an error message instead.