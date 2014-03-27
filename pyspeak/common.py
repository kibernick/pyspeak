from settings import MAX_WORD_LEN


class UnknownLanguageException(Exception):
    def __init__(self, lang):
        self.lang = lang
    def __str__(self):
        return "Language not recognized: " + repr(self.lang)


class KeywordsNumberException(Exception):
    def __init__(self, n_kwords):
        self.n_kwords = n_kwords
    def __str__(self):
        return "Invalid number of keywords to import: " + repr(self.n_kwords)


class MinKeywordLengthException(Exception):
    def __init__(self, min_word_len):
        self.min_word_len = min_word_len
    def __str__(self):
        msg = "Invalid minimum keyword length (%s), needs to be between 0 and %s: "
        return msg % (repr(self.min_word_len), MAX_WORD_LEN)