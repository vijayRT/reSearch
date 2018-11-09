from graph_tool.all import *
import os
from os import scandir
import json
import time
def calcpagerank():
    g = Graph()
    cwd = os.path.dirname(os.path.realpath(__file__))
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
    count = 0
    stringprop = g.new_vertex_property("string")
    for entry in scandir(dataDirPath):
        if not entry.name.startswith('.') and entry.is_file():
            filepath = entry.path
            count += 1
            if os.path.getsize(filepath) > 0:
                with open(filepath, "r", encoding='utf-8') as f:
                    jsonobj = json.load(f)
                    id = jsonobj['index']
                    idnode = g.add_vertex()
                    stringprop[idnode] = id
                    for reference in jsonobj['references']:
                        print(id, reference)
                        refnode = g.add_vertex()
                        stringprop[refnode] = reference
                        g.add_edge(idnode, refnode)

    pr = pagerank(g)
    for v in g.get_vertices():
        jsonfile = os.path.join(dataDirPath, stringprop[v] + ".json")
        print(jsonfile)
        with open(jsonfile, "r+", encoding="utf-8") as f:
            jsonobj = json.load(f)
            jsonobj["pagerank"] = pr[v]
            f.seek(0)
            f.truncate()
            json.dump(jsonobj, f)
calcpagerank()