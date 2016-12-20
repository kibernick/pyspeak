[![Build Status](https://api.travis-ci.org/kibernick/pyspeak.png)](https://travis-ci.org/kibernick/pyspeak)

# pyspeak
The aim is to do rough language classification of a continuous stream of documents, using keyword matching.

Note: This is an old project that has been bumped to use the latest `ahocorasick` library. 

For this we are using the `pyahocorasick` library which implements the Aho-Corasick automatons, that are commonly used for fast multi-pattern matching in intrusion detection systems (such as snort), anti-viruses and many other applications that need fast matching against a pre-defined set of string keys.

The program is given a set of languages, and for each language a list of keywords. The program will say for each document, in which language is its text (or "I don't know"), based on whether it finds any keywords it knows. The idea is to be able to have many rules like this "If the text contains rijkswaterstaat it's in dutch", "If it contains Deutsche it's in german" etc.

## Dependencies
* [pyahocorasick](https://pypi.python.org/pypi/pyahocorasick/) (or `pip install pyahocorasick`)
* [ipython](https://pypi.python.org/pypi/ipython) (optional, for data wrangling) 

## Usage
* Simple run with default values: `python main.py`. Writes to standard output for each tweet: *detected language*, *actual language*, *tweet content*.
* List all command line options with `python main.py -h`.

### Sample output
```
$ python main.py
en (en) Madonna's New Song Could Drop Any Second! Be Still, Our Rebel Heart! h
en (en) Warner Bros. to preview The Hobbit: There and Back Again at CinemaCon
...
nl (nl) Ik wil nu heel dicht bij jou zijn<3
nl (nl) Gezond eten is echt moeilijk.
...
en (de) Vielen Dank an unsere Fans für die großartige Atmosphäre und einen
de (de) Coverdownload nur nach Login. Haben manche Verlage Angst davor, dass j 
```

### Command-line configuration
You can override the maximum number of keywords to load with `--max_kwords`, as well as the minimum keyword length to consider with `--min_kword_len`.

### Additional configuration
Check out `pyspeak/settings.py`. Also see below.

## Input data
* Keywords obtrainted from University of Leipzig Frequency Lists: [nl](http://wortschatz.uni-leipzig.de/Papers/top100nl.txt) [en](http://wortschatz.uni-leipzig.de/Papers/top100en.txt) [de](http://wortschatz.uni-leipzig.de/Papers/top100de.txt) [fr](http://wortschatz.uni-leipzig.de/Papers/top100fr.txt).
* Tweets obtained from https://twitter.com/search, under search terms "lang:nl", "lang:en", etc. Selected first 20 tweets in each language, so that we "know" they are in that language (vague tweets like "OK" ignored for now, may be used for testing and experiments later). For now assume short documents, so just analysing the whole "document" (or tweet in this case) is fine.

## Solution
* Each document has a "score" for each language we are looking up. This score could be just a counter of how many keywords were found in a document, or perhaps something that also takes into account that a word was found in language A but not in language B, etc. For now, maximum score determines the inferred language.
* Disregarding the case where there are multiple languages in one sentence. One classification result per input-text.
* Makes use of an implementation of the [Aho–Corasick string matching algorithm](https://hkn.eecs.berkeley.edu/~dyoo/python/ahocorasick/), for fast multiple keyword/phrase search in texts. Runs for each incoming document per keyword set, and get scores that way.
* Solution implemented as a single-run script for now.
