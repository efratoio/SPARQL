import re
from collections import namedtuple
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import numpy

Entry = namedtuple('Entry', 'instance predicate concept')

def get_entries(path):
	entries = []
	with open(path) as file:
		for line in file:
			if False == line.startswith('#@'): # an entry doesn't starts with `#@` line
				entryArr = line[:-2].split()
				entries.append( Entry._make(entryArr) )            
	return entries

                
def make_graph(entries):
	g = nx.DiGraph()
	#vertices
	v1 = [getattr(entry, 'instance') for entry in entries]
	v2 = [getattr(entry, 'concept') for entry in entries]
	for i in range(len(v1)):
		g.add_node(v1[i], name=v1[i])
		g.add_node(v2[i], name=v2[i])
	#edges
	g.add_edges_from([(v1[i],v2[i], {'pred' : getattr(entries[i], 'predicate')}) for i in range (len(v1))])
	return g


def draw_graph(g):
	pos=nx.spring_layout(g)
	nx.draw(g, pos)
	node_labels = dict([((u),d['name']) for u,d in g.nodes(data=True)]) # node labels
	nx.draw_networkx_labels(g, pos, labels = node_labels)
	edge_labels = dict([((u,v,),d['pred']) for u,v,d in g.edges(data=True)])  # edge labels
	nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels)
	plt.show() # show graph


def simrank(G, r=0.8, max_iter=100, eps=1e-4):

    nodes = G.nodes()
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = numpy.zeros(len(nodes))
    sim = numpy.identity(len(nodes))

    for i in range(max_iter):
        if numpy.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = numpy.copy(sim)
        for u, v in itertools.product(nodes, nodes):
            if u is v:
                continue
            u_ns, v_ns = G.predecessors(u), G.predecessors(v)

            # evaluating the similarity of current iteration nodes pair
            if len(u_ns) == 0 or len(v_ns) == 0: 
                # if a node has no predecessors then setting similarity to zero
                sim[nodes_i[u]][nodes_i[v]] = 0
            else:                    
                s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
                sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / (len(u_ns) * len(v_ns))


    return sim


# g = make_graph(get_entries('yagofactssubset.ttl'))
# print(simrank(g))

# #draw_graph(g)
