import os
import json
import copy

cwd = os.path.dirname(os.path.realpath(__file__))
filedir = os.path.join(cwd, os.path.pardir, "dblpfiledir")

sourcefile = os.path.join(cwd, os.path.pardir, "outputacm.txt")

switcher = {
    "#*": "title",
    "#@": "author",
    "#t": "year",
    "#c": "venue",
    "#i": "index",
    "#!": "abstract",
    "#%": "references"
}

emptyjsonobj = {
        "title": "",
        "author": "",
        "year": "",
        "venue": "",
        "index": "",
        "abstract": "",
        "references": []
    }
with open(sourcefile, "r", encoding="utf-8") as f:
    jsonobj = copy.deepcopy(emptyjsonobj)
    for line in f:
        prefix = line[:2]
        linecontent = line[2:].rstrip("\n")
        if prefix != "\n":
            if prefix == "#%":
                jsonobj["references"].append(linecontent)
            else:
                jsonobj[switcher[prefix]] = linecontent
        else:
            jsonobj["index"] = jsonobj["index"][4:]
            print(jsonobj["index"])
            jsonfilepath = os.path.join(filedir, jsonobj["index"] + ".json")
            jsonfile = open(jsonfilepath, "w", encoding="utf-8")
            json.dump(jsonobj, jsonfile, indent=4)
            jsonfile.close()
            jsonobj = copy.deepcopy(emptyjsonobj)
        
        