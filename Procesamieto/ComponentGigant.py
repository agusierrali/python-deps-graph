import networkx as nx, json
import pypistats
from base64 import b64decode
import csv
import operator
import numpy as np
import pandas as pd

#Remueve los nodos que no pertenecen a la componente gigante
GigantComponent = pd.read_csv("ComponenteGigante.csv",sep=",",dtype=str)
G4 = nx.read_gml('../grafos/graphv4.gml')
G3 = nx.read_gml('../grafos/graphv4.gml')
G32 = nx.read_gml('../grafos/graphv4.gml')
for n in G3:
    if not(n in list(GigantComponent["Label"])):
        G4.remove_node(n)
        G32.remove_node(n)
       
nx.write_gml(G32, '../grafos/graphv5.gml')
nx.write_gml(G4, '../grafos/graphv6.gml')