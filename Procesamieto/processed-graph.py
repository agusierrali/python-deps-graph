import networkx as nx, json
import pypistats
from base64 import b64decode
import csv
import operator


def delete_nodes():
    delete=[]
    G = nx.read_gml('../grafos/graphv2.gml')
    for n in G:
        try:
            G.nodes[n]["p"]
        except:
            delete+= [(n)]

    for node in delete:
        G.remove_node(node)

    nx.write_gml(G, '../grafos/graphv3.gml')

def add_popularity():
    delete=[]
    G = nx.read_gml('../grafos/graphv2.gml')
    for n in G:
        try:
            G.nodes[n]["p"]
        except:
            try:
                p=pypistats.recent(n, "month", format="json")
                popularity = json.loads(p)
                G.nodes[n]["p"]=popularity["data"]["last_month"]
                print("no",n)
            except:
                delete+= [(n)]
    
    for node in delete:
        G.remove_node(node)

    nx.write_gml(G, '../grafos/graphv3-1.gml')
            

def max_p():
    G = nx.read_gml('../grafos/graphv3-1.gml')
    p=0
    for n in G:
       if (p <= int(G.nodes[n]["p"])):
           p=G.nodes[n]["p"]
    return p

def min_p():
    G = nx.read_gml('../grafos/graphv3-1.gml')
    p=max_p()
    baja="none"
    for n in G:
       if (p > int(G.nodes[n]["p"])):
            p=G.nodes[n]["p"]
            baja=n
    return p,baja

def create_graph_range():
    G = nx.read_gml('../grafos/graphv3-1.gml')
    alta=[]
    muyalta=[]
    for n in G:
        p=G.nodes[n]["p"]
        if (p<=22288041):
            G.nodes[n]["p"]="baja"
        elif ((p>22288041)and(p<=44576082)):
            G.nodes[n]["p"]="media"
        elif ((p>44576082)and(p<=66864123)):
            G.nodes[n]["p"]="alta"
            alta.append(n)
        else:
            G.nodes[n]["p"]="muyalta"
            muyalta.append(n)
    nx.write_gml(G, 'graphv4.gml')
    return alta,muyalta

def CentralityBetweenness(G,baja,alta,muyalta):
    b=nx.betweenness_centrality(G)
    mi=(b[min(b, key=b.get)] , min(b, key=b.get))
    ma=(b[max(b, key=b.get)] , max(b, key=b.get))
    praltas=[]
    prmuyaltas=[]
    prbaja=[]
    for item in b:
        if str(item) in alta:
            praltas.append((b[item],item))
        elif str(item) in muyalta:
            prmuyaltas.append((b[item],item))
        elif str(item) == baja:
            prbaja.append((b[item],item))
    return mi,ma,prbaja,praltas,prmuyaltas

def HIT(G,baja,alta,muyalta):
    hit=nx.hits(G,max_iter=500)
    h=hit[0]
    mi=(h[min(h, key=h.get)] , min(h, key=h.get))
    ma=(h[max(h, key=h.get)] , max(h, key=h.get))
    praltas=[]
    prmuyaltas=[]
    prbaja=[]
    for item in h:
        if str(item) in alta:
            praltas.append((h[item],item))
        elif str(item) in muyalta:
            prmuyaltas.append((h[item],item))
        elif str(item) == baja:
            prbaja.append((h[item],item))
    return mi,ma,prbaja,praltas,prmuyaltas

def PageRanck(G,baja,alta,muyalta):
    p=nx.pagerank(G)
    mi=(p[min(p, key=p.get)] , min(p, key=p.get))
    ma=(p[max(p, key=p.get)] , max(p, key=p.get))
    praltas=[]
    prmuyaltas=[]
    prbaja=[]
    for item in p:
        if str(item) in alta:
            praltas.append((p[item],item))
        elif str(item) in muyalta:
            prmuyaltas.append((p[item],item))
        elif str(item) == baja:
            prbaja.append((p[item],item))
    return mi,ma,prbaja,praltas,prmuyaltas

def CentralityCloseness(G,baja,alta,muyalta):
    c=nx.closeness_centrality(G)
    print(c)
    mi=(c[min(c, key=c.get)] , min(c, key=c.get))
    ma=(c[max(c, key=c.get)] , max(c, key=c.get))
    praltas=[]
    prmuyaltas=[]
    prbaja=[]
    for item in c:
        if str(item) in alta:
            praltas.append((c[item],item))
        elif str(item) in muyalta:
            prmuyaltas.append((c[item],item))
        elif str(item) == baja:
            prbaja.append((c[item],item))
    return mi,ma,prbaja,praltas,prmuyaltas

def ProcesamientoCentralityC():
    G3 = nx.read_gml('../grafos/graphv3-1.gml')
    G4 = nx.read_gml('../grafos/graphv4.gml')
    alta,muyalta=create_graph_range()
    _,baja=min_p()
    mi,ma,cbaja,caltas,cmuyaltas=CentralityCloseness(G3,baja,alta,muyalta)
    print("El nodo con CC mas bajo es:",mi,"Con Popularidad:",G3.nodes[mi[1]]["p"],G4.nodes[mi[1]]["p"])
    print("El nodo con CC mas alto es:",ma,"Con Popularidad:",G3.nodes[ma[1]]["p"],G4.nodes[ma[1]]["p"])
    print("#cbaja#",cbaja)
    print("#caltas#",caltas)
    print("#cmuyaltas#",cmuyaltas)

def ProcesamientoPR():
    G3 = nx.read_gml('../grafos/graphv3-1.gml')
    G4 = nx.read_gml('../grafos/graphv4.gml')
    alta,muyalta=create_graph_range()
    _,baja=min_p()
    mi,ma,prbaja,praltas,prmuyaltas=PageRanck(G3,baja,alta,muyalta)
    print("El nodo con PR mas bajo es:",mi,"Con Popularidad:",G3.nodes[mi[1]]["p"],G4.nodes[mi[1]]["p"])
    print("El nodo con PR mas alto es:",ma,"Con Popularidad:",G3.nodes[ma[1]]["p"],G4.nodes[ma[1]]["p"])
    print("#prbaja#",prbaja)
    print("#praltas#",praltas)
    print("#prmuyaltas#",prmuyaltas)

def ProcesamientoHIT():
    G3 = nx.read_gml('../grafos/graphv3-1.gml')
    G4 = nx.read_gml('../grafos/graphv4.gml')
    alta,muyalta=create_graph_range()
    _,baja=min_p()
    mi,ma,hbaja,haltas,hmuyaltas=HIT(G3,baja,alta,muyalta)
    print("El nodo con hit mas bajo es:",mi,"Con Popularidad:",G3.nodes[mi[1]]["p"],G4.nodes[mi[1]]["p"])
    print("El nodo con hit mas alto es:",ma,"Con Popularidad:",G3.nodes[ma[1]]["p"],G4.nodes[ma[1]]["p"])
    print("#hbaja#",hbaja)
    print("#haltas#",haltas)
    print("#hmuyaltas#",hmuyaltas)

def ProcesamientoCentralityB():
    G3 = nx.read_gml('../grafos/graphv3-1.gml')
    G4 = nx.read_gml('../grafos/graphv4.gml')
    alta,muyalta=create_graph_range()
    _,baja=min_p()
    mi,ma,cbbaja,cbaltas,cbmuyaltas=CentralityBetweenness(G3,baja,alta,muyalta)
    print("El nodo con CB mas bajo es:",mi,"Con Popularidad:",G3.nodes[mi[1]]["p"],G4.nodes[mi[1]]["p"])
    print("El nodo con CB mas alto es:",ma,"Con Popularidad:",G3.nodes[ma[1]]["p"],G4.nodes[ma[1]]["p"])
    print("#cbbaja#",cbbaja)
    print("#cbaltas#",cbaltas)
    print("#cbmuyaltas#",cbmuyaltas)

def main():
    print("##########################Betwenness Centrality############################")
    print("/n")
    ProcesamientoCentralityB()
    print("/n")
    print("##########################Closeness Centrality############################")
    print('/n')
    ProcesamientoCentralityC()
    print('/n')
    print("##########################Page Rank############################")
    print('/n')
    ProcesamientoPR()
    print('/n')
    print("##########################HITS############################")
    print('/n')
    ProcesamientoHIT()
    print('/n')
    G3 = nx.read_gml('graphv3-1.gml')
    print(G3.degree('numpy'))

    
if __name__ == "__main__":
   main()