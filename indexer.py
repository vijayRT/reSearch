import os, os.path
from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(path=ID(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = create_in("indexdir", schema)

writer = ix.writer()
for path, directories, files in os.walk('.\data'):
    for file in files:
        filepath = os.path.join(path, file)
        with open(filepath, "r", encoding='utf-8') as f:
            writer.add_document(path=filepath, content=f.read())
            print("Indexed filename: ", filepath)
writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("sequential")
    results = searcher.search(query)
    print(results)
