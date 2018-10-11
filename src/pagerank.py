import networkx as nx
import matplotlib.pyplot as plt
import os
import json
from secrets import randbelow
def constructDiGraph():
    G = nx.DiGraph()

    cwd = os.path.dirname(os.path.realpath(__file__))
    dataDirPath = os.path.join(cwd, os.path.pardir, "dblpfiledir")
    for path, directories, files in os.walk(dataDirPath):
        for file in files:
            filepath = os.path.join(path, file)
            if os.path.getsize(filepath) > 0:
                with open(filepath, "r", encoding='utf-8') as f:
                    jsonobj = json.load(f)
                    id = jsonobj['id']
                    for reference in jsonobj['references']:
                        G.add_edge(reference, id)
    nx.draw(G, with_labels=False)
    jsongraph = nx.node_link_data(G)
    print(json.dumps(jsongraph, indent=4))
    plt.draw()
    plt.show()

for i in range(0, 50):
    print(randbelow(1000))