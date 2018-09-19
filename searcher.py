from whoosh.index import create_in, open_dir
from whoosh.fields import *

from whoosh.qparser import QueryParser

ix = open_dir("./indexdir")
with ix.searcher() as searcher:
    query = QueryParser("content", schema=ix.schema).parse("first")
    results = searcher.search(query)
    for result in results:
        print(result)