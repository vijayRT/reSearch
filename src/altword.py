from gensim.models import FastText
from gensim.test.utils import get_tmpfile
import Stemmer
import pandas as pd
import string
import os
from os import scandir
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def constructModelFromVldb():
    #stemmer = Stemmer.Stemmer("english")
    fname = open("./fasttext.model", "wb")
    conference_filenames = ["./vldb_id.txt", "./icse_id.txt", "./sigmod_id.txt"]
    words = []
    for filename in conference_filenames:
        data = pd.read_csv(filename, sep="\t", header=None)
        data.columns = ["id", "title", "unformattedtitle", "year", "date", "doi", "category", "categoryabbr", "hex1", "hex2", "number"]
        titles = list(data["title"])
        for title in titles:
            title = ''.join(ch for ch in title if ch not in exclude)
            titlewords = title.split(" ")
            titlewords = [w for w in titlewords if not w in stop_words]
            #titlewords = stemmer.stemWords(titlewords)
            words.append(titlewords)
    for word in words:
        print(word)
    modelF = FastText(words, size=4, window=5, min_count=1, iter=10)
    modelF.save(fname)
    fname.close()

def constructModelFromCiteseer():
    fname = open("./citeseerfasttext.model", "wb")
    cwd = os.path.dirname(os.path.realpath(__file__))
    dataDirPath = os.path.join(cwd, os.path.pardir, "citeseerdata")
    words = []
    sentences = []
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation).union(set(string.digits))
    for entry in scantree(dataDirPath):
        if not entry.name.startswith('.') and entry.is_file():
            filepath = entry.path
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().split(". ")
                for line in content:
                    sentence = cleanuptext(line)
                    print(sentence)
                    print("\n\n\n\n")
                    if len(sentence) is not 0:
                        sentences.append(sentence)
    modelF = FastText(sentences, size=4, window=4, min_count=1, iter=10)
    modelF.save(fname)
    fname.close()

def getSimilarWords(word):
    stemmer = Stemmer.Stemmer("english")
    modelF = FastText.load("./citeseerfasttext.model")
    print(modelF.wv.most_similar(stemmer.stemWord(word)))
    #print(modelF.wv.most_similar(word))

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry

def cleanuptext(text):
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    stop_words = set(stopwords.words('english'))
    sentences = word_tokenize(text)
    # content = ''.join(ch for ch in content if ch not in exclude)
    # contentwords = content.split(" ")
    # contentwords = [w for w in contentwords if not w in stop_words]
    sentences = [w for w in sentences if not w in stop_words]
    sentences = [w.replace("\n", " ") for w in sentences]
    sentences = [w for w in sentences if w.isalpha()]
    return sentences

#constructModelFromCiteseer()
getSimilarWords("artificial")
