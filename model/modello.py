import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._percorsoOpt=[]
        self._costoOpt=0

    def getAllCountries(self):
        return DAO.getAllCountries()

    def buildGraph(self, country, anno):
        self._graph = nx.Graph()
        nodes=DAO.getAllRetailers(country)
        self._graph.add_nodes_from(nodes)
        self.getAllArchi(anno)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllArchi(self, anno):
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u!=v:
                    peso=DAO.getAllArchi(u.Retailer_code, v.Retailer_code, anno)
                    if peso is not None:
                        self._graph.add_edge(u,v,weight=peso)

    def getVolumeDiVendita(self):
        lista=[]
        for n in self._graph.nodes:
            count=0
            vicini=self._graph.neighbors(n)
            for v in vicini:
                count+=self._graph[n][v]['weight']
            lista.append((n, count))

        lista.sort(key=lambda x:x[1], reverse=True)
        return lista

    def getPercorsoOpt(self, num):
        self._percorsoOpt=[]
        self._costoOpt=0.0
        for n in self._graph.nodes:
            self._ricorsione([n],num)
        return self._percorsoOpt, self._costoOpt

    def getPeso(self, u,v):
        return self._graph[u][v]['weight']

    def calcolaCosto(self, parziale):
        costo=0
        for i in range(0,len(parziale)-1):
            costo+=self._graph[parziale[i]][parziale[i+1]]['weight']
        return costo

    def _ricorsione(self, parziale, num):
        if len(parziale)==num+1:
            if parziale[0]!=parziale[-1]:
                return
            else:
                costo=self.calcolaCosto(parziale)
                if costo>self._costoOpt:
                    self._percorsoOpt=copy.deepcopy(parziale)
                    self._costoOpt=costo
                    return
        else:
            if len(parziale)==num:
                for n in self._graph.neighbors(parziale[-1]):
                    if parziale[0]==n:
                        parziale.append(n)
                        self._ricorsione(parziale, num)
                        parziale.pop()
            else:
                for n in self._graph.neighbors(parziale[-1]):
                    if n not in parziale:
                        parziale.append(n)
                        self._ricorsione(parziale, num)
                        parziale.pop()



if __name__=="__main__":
    myModel=Model()
    myModel.buildGraph("France", 2015)
    print(f"Num nodi: {myModel.getNumNodes()}; Num archi: {myModel.getNumEdges()}")
    lista=myModel.getVolumeDiVendita()
    path, costo=myModel.getPercorsoOpt(5)
    print(costo)
    for i in range(0, len(path)-1):
        print(str(path[i])+str(path[i+1]))
