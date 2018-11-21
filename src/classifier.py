import pandas as pd
import fasttext
import os
import json
from os import scandir

def prepTrainingData():
    conference_filenames = ["./vldb_id.txt", "./icse_id.txt", "./sigmod_id.txt"]
    words = []
    classifierfile = open("trainingclassifier.txt", "w")
    for filename in conference_filenames:
        data = pd.read_csv(filename, sep="\t", header=None)
        data.columns = ["id", "title", "unformattedtitle", "year", "date", "doi", "category", "categoryabbr", "hex1", "hex2", "number"]
        for index, row in data.iterrows():
            classifierfile.write("__label__" + row["categoryabbr"] + " " + row["unformattedtitle"] + "\n")
    classifierfile.close()


def classifierTraining():
    classifier = fasttext.supervised("trainingclassifier.txt", "model", lr=0.1, word_ngrams=1, epoch=15)
    text = ["Bipolar possibility theory in preference modeling: Representation, fusion and optimal solutions"]
    print(classifier.predict(text))

def predictClasses():
    model = fasttext.supervised("trainingclassifier.txt", "model", lr=0.1, word_ngrams=1, epoch=15)
    cwd = os.path.dirname(os.path.realpath(__file__))
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
    for entry in scantree(dataDirPath):
        if not entry.name.startswith('.') and entry.is_file():
            filepath = entry.path
            with open(filepath, "r+", encoding="utf-8") as f:
                jsoncontent = json.load(f)
                title = [jsoncontent["title"]]
                jsoncontent["category"] = model.predict(title)[0][0]
                f.seek(0)
                f.truncate()
                json.dump(jsoncontent, f, indent=4)

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  # see below for Python 2.x
        else:
            yield entry

predictClasses()