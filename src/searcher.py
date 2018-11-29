from whoosh.index import open_dir
from whoosh.highlight import UppercaseFormatter
import json
import os
from whoosh.qparser import QueryParser, MultifieldParser
from altword import getSimilarWords
import autocomplete
from spellchecker import SpellChecker
from gensim.models.doc2vec import Doc2Vec

class Search:
    def __init__(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        indexDirPath = os.path.join(cwd, os.path.pardir, "acmindexdir")
        self.dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
        self.ix = open_dir(indexDirPath)
        self.d2v_model = Doc2Vec.load("./d2vmodel.bin")
        self.spell = SpellChecker(distance=1)

    def searchdblp(self, userquery):
        documentNumber = 1
        finalresults = {
            "searchTerm": userquery,
            "searchquerydocuments": [],
            "relatedquerydocuments": []
        }

        similarwords = getSimilarWords(userquery.replace('"', '').replace(" ", ""))
        queries = []
        queries.append(userquery)
        for similarword in similarwords:
            queries.append(similarword[0])

        with self.ix.searcher() as searcher:
            queryparser = QueryParser("content", schema=self.ix.schema)
            for queryString in queries:
                parsedquery = queryparser.parse(queryString)

                if queryString == queries[0]:
                    corrected = searcher.correct_query(parsedquery, queryString)
                    print(corrected.string)
                    if corrected.query != parsedquery:
                        print("Did you mean:", corrected.string)

                results = searcher.search(parsedquery)
                results.formatter = UppercaseFormatter(between="~")

                for hit in results:
                    filename = hit["path"] + ".json"
                    filepath = os.path.join(self.dataDirPath, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        subresult = {}
                        jsonfile = json.load(f)
                        filecontents = jsonfile['abstract']
                        pagerank = jsonfile['pagerank']
                        category = jsonfile['category']
                        subresult = {
                            "title": hit['title'],
                            "path": "http://127.0.0.1:5000/file/" + hit["path"],
                            "highlights": ' ... '.join([x.replace("\n", " ") for x in ("".join(hit.highlights("content", filecontents)).split("~"))]),
                            "pagerank": pagerank,
                            "category": category
                        }
                        documentNumber += 1
                        if(queryString == userquery):
                            finalresults["searchquerydocuments"].append(subresult)
                        else:
                            finalresults["relatedquerydocuments"].append(subresult)
        return json.dumps(finalresults, indent=4)


    def getFileFromDir(self, filename):
        filename = filename + ".json"
        filecontents = ""
        filepath = os.path.join(self.dataDirPath, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            jsonobj = json.load(f)
            referencetitleslist = []
            for reference in jsonobj['references']:
                referencefilename = reference + ".json"
                referencefilepath = os.path.join(self.dataDirPath, referencefilename)
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
    
    def getSimilarDocuments(self, fileid):
        similardoctuple = self.d2v_model.docvecs.most_similar(fileid)
        similardocs = []
        for similardocitem in similardoctuple:
            similardocs.append(similardocitem[0])

        finalresults = {
            "searchquerydocuments": []
        }
        for docid in similardocs:
            filepath = os.path.join(self.dataDirPath, docid + ".json")
            with open(filepath, "r", encoding="utf-8") as f:
                subresult = {}
                jsonfile = json.load(f)
                filecontents = jsonfile['abstract']
                pagerank = jsonfile['pagerank']
                category = jsonfile['category']
                subresult = {
                    "title": jsonfile['title'],
                    "path": "http://127.0.0.1:5000/file/" + jsonfile["index"],
                    "highlights": jsonfile["abstract"][:100] + '...',
                    "pagerank": pagerank,
                    "category": category
                }
                finalresults["searchquerydocuments"].append(subresult)
        return json.dumps(finalresults, indent=4)