import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.nodes = []
    def load_interazione(self):
        self.interazione = DAO.get_interazione()
        return self.interazione     #dict di tuple (gene1, gene2)

    def load_cromosomi(self):
        self.cromosomi = DAO.get_cromosomi()
        return self.cromosomi

    def load_geni(self):
        self.geni = DAO.get_geni()
        return self.geni

    def get_nodes(self):
        self.load_cromosomi()

        for c in self.cromosomi:        #16
            self.G.add_node(c['cromosoma'])
            self.nodes.append(c['cromosoma'])
        return self.G


    def get_edges(self):
        self.edges = []

        self.load_interazione()         # (gene1, gene2)   = corr
        self.load_geni()        # gene ,  cromosoma

        tuples = {}
        gene_crom = {g['gene']: g['cromosoma'] for g in self.geni}      #dict   'G234064': 1

        for (gene1 , gene2), corr in self.interazione.items():
            crom1 = gene_crom.get(gene1)
            crom2 = gene_crom.get(gene2)
            if crom1 and crom2 and crom1 != crom2:
                key = (crom1, crom2)
                chiavi= tuples.keys()
                if key in chiavi:
                    tuples[key] += float(corr)  #gia presente-> update corr
                else:
                    try: tuples[key] = float(corr)     #aggiungo
                    except KeyError: continue
        triples = []
        for (k1, k2), v in tuples.items():
            triples.append((k1, k2,v))

        self.G.add_weighted_edges_from(triples)
        print(triples)
        return self.G


    def build_graph(self):
        self.get_nodes()
        self.get_edges()
        edges = self.G.
        e_min = 0
        e_max = 0
        for key, v in edges:
            if v > e_max: e_max = v
            if v < e_min: e_min = v
        nodes = len(list(self.G.nodes()))
        n_edges = len(list(self.G.edges()))
        return nodes, n_edges, e_min, e_max

    def count_edges(self, input):
        edges = self.G.edges()
        n_edges_over = []
        n_edges_under = []
        for n, w in edges:
            if float(input) < w:
                n_edges_over.append(w)
            else:
                n_edges_under.append(w)
        self.edges_sub_graph = n_edges_over + n_edges_under
        return len(n_edges_over), len(n_edges_under)

    def ricerca_cammino(self, input):
        self.dist_ott = 0.0
        self.sol_ott = []
        soglia = input

        for n in self.nodes:      #condizione di terminazione anche
            # parametri: nodo  , lista di nodi della sol, lista di archi con info della sol
            self.ricorsione(n, [n], [], soglia)      #tot nodi
        print(f' soluzione ottima {self.sol_ott}')

        return self.sol_ott, self.dist_ott

    def ricorsione(self, node, partial_nodes, partial_edges, soglia):
        #update
        dist_cur = sum(e[2] for e in partial_edges)
        if dist_cur > self.dist_ott:
            self.dist_ott = dist_cur
            self.sol_ott = list(partial_edges)      #list di edges  con w (lista triplette)

        for n in list(self.G.neighbors(node)):
            #prima condition per 1' round
            if n not in partial_nodes:
                try:
                    peso = self.G[node][n]['weight']
                    print('3')
                    if peso > soglia:
                        print('1')
                        partial_edges.append((node, n, peso))
                        partial_nodes.append(n)
                        print('2')
                        self.ricorsione(n, partial_nodes, partial_edges, soglia)
                        #backtrack
                        partial_edges.pop()
                        partial_nodes.pop()
                except KeyError: continue           #non esiste arco tra nodi
            '''       
            else:       #1' round
                try:
                    peso = self.G[node][n]['weight']
                    print('3')
                    if peso > soglia:
                        print('1')
                        partial_edges.append((node, n, peso))
                        partial_nodes.append(n)
                        print('2')
                        self.ricorsione(n, partial_nodes, partial_edges, soglia)
                except KeyError: continue'''
















