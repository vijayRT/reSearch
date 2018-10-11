from whoosh.index import open_dir
from whoosh.highlight import UppercaseFormatter
import json
import os
from whoosh.qparser import QueryParser


def search(queryString):
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "indexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir)
    ix = open_dir(indexDirPath)
    documentNumber = 1
    finalresults = {
        "searchTerm": queryString,
        "documents": []
    }
    with ix.searcher() as searcher:
        query = QueryParser("content", schema=ix.schema).parse(queryString)
        results = searcher.search(query)
        results.formatter = UppercaseFormatter(between="~")
        for hit in results:
            filepath = os.path.join(dataDirPath, hit["path"])
            with open(filepath, "r", encoding="utf-8") as f:
                subresult = {}
                filecontents = f.read()
                subresult[str(documentNumber)] = {
                    "title": hit['title'],
                    "path": os.path.join("http://127.0.0.1:5000/file", filepath),
                    "highlights": [x.replace("\n", " ") for x in ("".join(hit.highlights("content", filecontents)).split("~"))]
                }
                documentNumber += 1
                finalresults["documents"].append(subresult)
    return json.dumps(finalresults, indent=4)
