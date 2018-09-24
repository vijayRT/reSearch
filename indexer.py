import os, os.path
from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(path=ID(stored=True), title=TEXT(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)
writer = ix.writer()

for path, directories, files in os.walk('.\data'):
    for file in files:
        filepath = os.path.join(path, file)
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
            title = content.split("\n")[0]
            writer.add_document(path=filepath, title=title, content=content)
            print("Indexed filename: ", filepath)
            print(title)
writer.commit()
