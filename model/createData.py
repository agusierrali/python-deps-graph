import networkx as nx, json
import pypistats
from base64 import b64decode
import csv
import operator
import numpy as np
import pandas as pd

def nodes_connected(u, v):
    return u in G4.neighbors(v)
    
GigantComponent = pd.read_csv("../ComponenteGigante.csv",sep=",",dtype=str)
G4 = nx.read_gml('../graphv6.gml')
G3 = nx.read_gml('../graphv5.gml')
c=nx.closeness_centrality(G3)
b=nx.betweenness_centrality(G3)
hit=nx.hits(G3,max_iter=500)
h=hit[0]
p=nx.pagerank(G3)
rows=list(range(0,len(GigantComponent["Id"])))
columns=['setuptools','six','Degree','HIT','Closeness','Betweenness','PageRank','classification']
N=[]
print(list(GigantComponent["Label"]))
for i in list(GigantComponent["Label"]):
    setuptools=nodes_connected(i,'setuptools')
    six=nodes_connected(i,'six')
    Degree=G4.degree[i]
    HIT=h[i]
    Closeness=c[i]
    Betweenness=b[i]
    PageRank=p[i]
    classification=G4.nodes[i]["p"]
    new=[setuptools,six,Degree,HIT,Closeness,Betweenness,PageRank,classification]
    N.append(new)

K=np.array(N) 
M=pd.DataFrame(K,columns=columns)
print(M)
M.to_csv('data.csv')
