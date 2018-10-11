import os, os.path
from whoosh.index import create_in
from whoosh.fields import *
import json
import time
import matplotlib.pyplot as plt
from secrets import randbelow
def dblpindextest():
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), author=TEXT, content=TEXT)
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "testindexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpdata", "dblp-ref")
    if not os.path.exists(indexDirPath):
        os.mkdir(indexDirPath)
    ix = create_in(indexDirPath, schema)
    writer = ix.writer()
    linelens = []
    times = []
    filepath = os.path.join(dataDirPath, "dblp-ref-3.json")
    with open(filepath, "r", encoding='utf-8') as f:
        for line in f:
            jsonline = json.loads(line)
            try:
                t1 = time.time()
                writer.add_document(title=jsonline['title'], path=jsonline['id'], content=jsonline['abstract'])
                t2 = time.time()
                if t2-t1 > 0:
                    times.append(t2-t1)
                    linelens.append(len(jsonline['abstract']))
                    print(len(line), t2-t1)
            except Exception as e:
                print(str(e))
    plotlens = []
    plottimes = []
    for i in range(0, 50):
        x = randbelow(1000)
        plotlens.append(linelens[x])
        plottimes.append(times[x])
    plt.scatter(plotlens, plottimes)
    plt.show()


def citeseerindextest():
    schema = Schema(path=ID(stored=True), title=TEXT(stored=True), content=TEXT)
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "testindexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir, "citeseerdata")
    if not os.path.exists(indexDirPath):
        os.mkdir(indexDirPath)

    ix = create_in(indexDirPath, schema)
    writer = ix.writer()
    linelens = []
    times = []
    for path, directories, files in os.walk(dataDirPath):
        for file in files:
            filepath = os.path.join(path, file)
            with open(filepath, "r", encoding='utf-8') as f:
                content = f.read()
                title = content.split("\n")[0]
                t1 = time.time()
                writer.add_document(path=filepath, title=title, content=content)
                t2 = time.time()
                linelens.append(len(content))
                times.append(t2-t1)
                print("Indexed filename: ", filepath)
                print(title)
    plotlens = []
    plottimes = []
    for i in range(0, 50):
        x = randbelow(1000)
        plotlens.append(linelens[x]/1000)
        plottimes.append(times[x])
    fig = plt.figure()
    plt.scatter(plotlens, plottimes)
    fig.suptitle('CiteSeer Data Indexing speed', fontsize=20)
    plt.xlabel('Size of document (KB)', fontsize=18)
    plt.ylabel('Time taken for indexing (ms)', fontsize=16)
    plt.show()

#dblpindextest()
citeseerindextest()