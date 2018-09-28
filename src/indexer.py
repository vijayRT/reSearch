import os, os.path
from whoosh.index import create_in
from whoosh.fields import *


def createindex():
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
