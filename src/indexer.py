import os, os.path
from whoosh.index import create_in
from whoosh.fields import *
import json

def citeseerindex():
    schema = Schema(path=ID(stored=True), title=TEXT(stored=True), content=TEXT)
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "indexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir, "data")
    if not os.path.exists(indexDirPath):
        os.mkdir(indexDirPath)

    ix = create_in(indexDirPath, schema)
    writer = ix.writer()

    for path, directories, files in os.walk(dataDirPath):
        for file in files:
            filepath = os.path.join(path, file)
            with open(filepath, "r", encoding='utf-8') as f:
                content = f.read()
                title = content.split("\n")[0]
                writer.add_document(path=filepath, title=title, content=content)
                print("Indexed filename: ", filepath)
                print(title)
    writer.commit()

def dblpindex():
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), author=TEXT, content=TEXT)
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "dblpindexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpdata")
    if not os.path.exists(indexDirPath):
        os.mkdir(indexDirPath)
    filedir = os.path.join(cwd, os.path.pardir, "dblpfiledir")
    ix = create_in(indexDirPath, schema)
    writer = ix.writer()
    for path, directories, files in os.walk(dataDirPath):
        for file in files:
            filepath = os.path.join(path, file)
            with open(filepath, "r", encoding='utf-8') as f:
                for line in f:
                    jsonline = json.loads(line)
                    modifiedjsonfilename = str(jsonline['id']) + ".json"
                    with open(os.path.join(filedir, modifiedjsonfilename), "w+") as m:
                        try:
                            modifiedjson = {
                                "id": jsonline['id'],
                                "title": jsonline['title'],
                                "authors": jsonline['authors'],
                                "abstract": jsonline['abstract'],
                                "references": jsonline['references'],
                                "venue": jsonline['venue'],
                                "year": jsonline['year'],
                                "numberOfCitations": jsonline['n_citation']
                            }
                            writer.add_document(title=jsonline['title'], path=jsonline['id'], content=jsonline['abstract'])
                            json.dump(modifiedjson, m, indent=4)
                            print('Success')
                        except Exception as e:
                            print(str(e))
    writer.commit()

dblpindex()