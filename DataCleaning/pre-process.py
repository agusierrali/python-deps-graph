import networkx as nx, json
import pypistats
from base64 import b64decode
import csv

data = []
G=nx.Graph()
count=0
previous=""
with open('pypi-processed.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "popularity", "deps"])
    with open('pypi-deps.csv', 'r') as file:
        for line in file:
            name, version, deps = line.split('\t')
            try:
                p=pypistats.recent(name, "month", format="json")
                if not(previous==name):
                    popularity = json.loads(p)
                    deps = json.loads(b64decode(deps))
                    writer.writerow([name,popularity["data"]["last_month"],deps])
                    data+= [(name, popularity["data"]["last_month"], deps)]
                previous=name
            except:
                    count+= 1
print(len(data))
for ex in data:
    name, popularity, deps = ex
#    G.add_node("%s-%s" % (name, popularity))
    G.add_node(name,p=popularity)
    for dep in deps:
#        if not '#' in dep: G.add_edge("%s-%s" % (name, popularity), dep.replace("\"", ""))
        if not '#' in dep: G.add_edge(name, dep.replace("\"", ""))

nx.write_gml(G, 'graph.gml')
