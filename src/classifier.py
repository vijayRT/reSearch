import pandas as pd
import fasttext
import os
import json
from os import scandir
import random

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


def prepareTestData():
    preparedfile = open("./trainingclassifier.txt", "r")
    train_file = open("./fasttexttrain.txt", "w")
    test_file = open("./fasttexttest.txt", "w")
    train = []
    test = []
    for line in preparedfile.readlines():
        if random.randint(1, 10) == 1:
            test.append(line)
        else:
            train.append(line)
    train_file.writelines(train)
    test_file.writelines(test)
    train_file.close()
    test_file.close()


def performTest():
    model = fasttext.supervised("fasttexttrain.txt", "testingmodel", lr=0.1, word_ngrams=1, epoch=15)
    with open("./fasttexttest.txt", "r") as f:
        lines = f.readlines()
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for line in lines:
            label = line.split(" ")[0].replace("__label__", "")
            line = line.replace(label + " ", '')
            predicition = model.predict(line)
            if predicition[0][0] == label and predicition[0][0] == "icse":
                tp += 1
            elif predicition[0][0] != label and predicition[0][0] == "icse":
                fp += 1
            elif predicition[0][0] != label and label == "icse":
                fn += 1
        tn = len(lines) - (tp + fp + fn)
        print("TP:", tp, "FP: ", fp, "TN: ", tn, "FN: ",fn)
                
    

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

performTest()