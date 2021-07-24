import networkx as nx, json
import pypistats
from base64 import b64decode
import csv
import operator
import numpy as np
import pandas as pd


G = nx.read_gml('../grafos/graphv4.gml')
N = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
M=pd.DataFrame(N,columns=['baja','media','alta','muy-alta'],index=['baja','media','alta','muy-alta'])
print(G.number_of_edges(),"Cantidad de aristas")
for e in G.edges():
    a,b=e
    if  G.nodes[a]["p"]=="baja":
        
        if  G.nodes[b]["p"]=="baja":
            #baja-baja 
            M['baja']['baja']= M['baja']['baja']+1
        elif  G.nodes[b]["p"]=="media":
            #baja-media
            M['baja']['media']= M['baja']['media']+1
        elif  G.nodes[b]["p"]=="alta":
            #baja-alta
            M['baja']['alta']= M['baja']['alta']+1
        else:
            #baja-muyalta
            M['baja']['muy-alta']= M['baja']['muy-alta']+1
            

    elif  G.nodes[a]["p"]=="media":

        if  G.nodes[b]["p"]=="baja":
            #media-baja 
            M['media']['baja']= M['media']['baja']+1
        elif  G.nodes[b]["p"]=="media":
            #media-media
            M['media']['media']= M['media']['media']+1
        elif  G.nodes[b]["p"]=="alta":
            #media-alta
            M['media']['alta']= M['media']['alta']+1
        else:
            #media-muyalta
            M['media']['muy-alta']= M['media']['muy-alta']+1
            
    elif  G.nodes[a]["p"]=="alta":
        
        if  G.nodes[b]["p"]=="baja":
            #alta-baja 
            M['alta']['baja']= M['alta']['baja']+1
        elif  G.nodes[b]["p"]=="media":
            #alta-media
            M['alta']['media']= M['alta']['media']+1
        elif  G.nodes[b]["p"]=="alta":
            #alta-alta
            M['alta']['alta']= M['alta']['alta']+1
        else:
            #alta-muyalta
            M['alta']['muy-alta']= M['alta']['muy-alta']+1

    else:
       
        if  G.nodes[b]["p"]=="baja":
            #muy-alta-baja 
            M['muy-alta']['baja']= M['muy-alta']['baja']+1
        elif  G.nodes[b]["p"]=="media":
            #muy-alta-media
            M['muy-alta']['media']= M['muy-alta']['media']+1
        elif  G.nodes[b]["p"]=="alta":
            #muy-alta-alta
            M['muy-alta']['alta']= M['muy-alta']['alta']+1
        else:
            #muy-alta-muyalta
            M['muy-alta']['muy-alta']= M['muy-alta']['muy-alta']+1

print(M)