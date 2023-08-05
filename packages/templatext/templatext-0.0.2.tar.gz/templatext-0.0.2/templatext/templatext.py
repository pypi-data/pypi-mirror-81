import re
import string

import spacy
import unidecode
import gensim.downloader as api

from word2number import w2n
from bs4 import BeautifulSoup

from .contractions import expand_contractions


punctuation_regex = re.compile("[%s]" % re.escape(string.punctuation))

class Templatext():
    def __init__(self, language="en", remove_html=True, extra_whitespace=True,
                accented_chars=True, contractions=True, lowercase=True, stop_words=True,
                punctuations=True, special_chars=True, remove_num=True, convert_num=True,
                lemmatization=True, punctuation=True, tokens=True):
        self.language = language
        self.remove_html = remove_html
        self.extra_whitespace = extra_whitespace
        self.accented_chars = accented_chars
        self.contractions = contractions
        self.lowercase = lowercase
        self.stop_words = stop_words
        self.punctuations = punctuations
        self.special_chars = special_chars
        self.remove_num = remove_num
        self.convert_num = convert_num
        self.lemmatization = lemmatization
        self.punctuation = punctuation
        self.tokens = tokens

        self.nlp = spacy.load('en_core_web_md')

    @staticmethod
    def strip_html_tags(text):
        """Remove HTML tags from text"""
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    @staticmethod
    def remove_whitespace(text):
        """Remove extra whitespaces from text"""
        text = text.strip()
        return " ".join(text.split())
    
    @staticmethod
    def remove_accented_chars(text):
        """Remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text
    
    @staticmethod
    def lower(text):
        """Convert text to lowercase"""
        return text.lower()

    @staticmethod
    def expand_contractions(text):
        """Expand contracted words, e.g. don't to do not"""
        text = expand_contractions(text)
        return text

    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from text"""
        return punctuation_regex.sub("", text)

    def preprocess(self, text):
        """Perform text preprocessing"""
        if self.remove_html:
            text = self.strip_html_tags(text)
        if self.extra_whitespace:
            text = self.remove_whitespace(text)
        if self.accented_chars:
            text = self.remove_accented_chars(text)
        if self.contractions:
            text = self.expand_contractions(text)
        if self.lowercase:
            text = self.lower(text)
        if self.punctuation:
            text = self.remove_punctuation(text)

        doc = self.nlp(text)
        clean_text = []

        for token in doc:
            flag = True
            edit = token.text
            if self.stop_words and token.is_stop and token.pos_ != 'NUM':
                flag = False
            if self.punctuations and token.pos_ == 'PUNCT' and flag:
                flag = False
            if self.special_chars and token.pos_ == 'SYM' and flag:
                flag = False
            if self.remove_num and (token.pos_ == 'NUM' or token.text.isnumeric()) and flag:
                flag = False
            if self.convert_num and token.pos_ == 'NUM' and flag:
                edit = w2n.word_to_num(token.text)
            elif self.lemmatization and token.lemma_ != "-PRON-" and flag:
                edit = token.lemma_
            if edit.strip() != "" and flag:
                clean_text.append(edit)

        return clean_text
        
