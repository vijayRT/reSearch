from whoosh.index import open_dir
from whoosh.highlight import UppercaseFormatter
import json
import os
from whoosh.qparser import QueryParser


def searchciteseer(queryString):
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

def searchdblp(queryString):
    cwd = os.path.dirname(os.path.realpath(__file__))
    indexDirPath = os.path.join(cwd, os.path.pardir, "dblpindexdir")
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
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
            filename = hit["path"] + ".json"
            filepath = os.path.join(dataDirPath, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                subresult = {}
                filecontents = json.load(f)['abstract']
                subresult[str(documentNumber)] = {
                    "title": hit['title'],
                    "path": "http://127.0.0.1:5000/file/" + hit["path"],
                    "highlights": [x.replace("\n", " ") for x in ("".join(hit.highlights("content", filecontents)).split("~"))]
                }
                documentNumber += 1
                finalresults["documents"].append(subresult)
    return json.dumps(finalresults, indent=4)


def getFileFromDir(filename):
    cwd = os.path.dirname(os.path.realpath(__file__))
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
    filename = filename + ".json"
    filecontents = ""
    filepath = os.path.join(dataDirPath, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        jsonobj = json.load(f)
        referencetitleslist = []
        for reference in jsonobj['references']:
            referencefilename = reference + ".json"
            referencefilepath = os.path.join(dataDirPath, referencefilename)
            with open(referencefilepath, "r", encoding="utf-8") as referencefile:
                fileread = referencefile.read()
                print(referencefilepath, len(fileread))
                if len(fileread) > 0:
                    referenceObj = json.loads(fileread)
                    referencedata = {
                        "title": referenceObj['title'],
                        "path": "http://127.0.0.1:5000/file/" + reference
                    }
                    referencetitleslist.append(referencedata)
        jsonobj['references'] = referencetitleslist
        filecontents = json.dumps(jsonobj)
    return filecontents