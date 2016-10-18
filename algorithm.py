

import parse_rdf as pr
import parse_ttl as pt 
from rdflib import URIRef
import pickle


def common_out_neighbors(g, i, j):
    return [x for x in set(g.successors(i)).intersection(g.successors(j)) if  \
    	str(g[i][x]['triples'][0][1]) == str(g[j][x]['triples'][0][1])] 

def common_in_neighbors(g, i, j):
    return [x for x in set(g.predecessors(i)).intersection(g.predecessors(j)) if  \
    	str(g[x][i]['triples'][0][1]) == str(g[x][j]['triples'][0][1])] 

def create_setting():
	print "graph"
	g_nt = pr.make_graph("pl/pl_types.ttl",format="turtle")
	with open("pl/g_nt","w") as f:
		pickle.dump(g_nt,f)

	print "sim"
	sim = pr.simrank(g_nt)

	with open("pl/sim","w") as f:
		pickle.dump(sim,f)

	print "prank"
	simp = pr.psimrank(g_nt)

	with open("pl/simp","w") as f:
		pickle.dump(simp,f)


def explore_node(g_nt,node):
	print "node name: "+str(node)

	print str(node) +" in neighbours:\n"
	for n in g_nt.predecessors(node):
		print "\t"+str(g_nt[n][node]['triples'][0][1])+" : "+str(g_nt[n][node]['triples'][0][2])+"\n"
	
	print str(node) +" out neighbours:\n"
	for n in g_nt.successors(node):
		print "\t"+str(g_nt[node][n]['triples'][0][1])+" : "+str(g_nt[node][n]['triples'][0][2])+"\n"
	
def compare_nodes(g_nt,node1,node2,sim,simp):
	print "common in neighbours:"
	nodes = sorted(g_nt.nodes())
	common_in =  common_in_neighbors(g_nt,node1,node2)
	for n in common_in:
		print str(g_nt[node1][n]['triples'][0][1])+" : "+str(g_nt[node1][n]['triples'][0][2])+"\n"
		print "simrank node1: "+str(sim.item(nodes.index(node1),nodes.index(n)))
		print "prank: node1"+str(simp.item(nodes.index(node1),nodes.index(n)))

		print "simrank node2: "+str(sim.item(nodes.index(node2),nodes.index(n)))
		print "prank: node2"+str(simp.item(nodes.index(node2),nodes.index(n)))

	print "common out neighbours:"

	common_out= common_out_neighbors(g_nt,node1,node2)
	for n in common_out:
		print str(g_nt[node1][n]['triples'][0][1])+" : "+str(g_nt[node1][n]['triples'][0][2])+"\n"
		print "simrank node 1: "+str(sim.item(nodes.index(node1),nodes.index(n)))
		print "prank node 1: "+str(simp.item(nodes.index(node1),nodes.index(n)))

		print "simrank node 2: "+str(sim.item(nodes.index(node2),nodes.index(n)))
		print "prank node 2: "+str(simp.item(nodes.index(node2),nodes.index(n)))

def run_alg():
	g_nt = None
	with open("pl/g_nt") as f:
		g_nt =pickle.load(f)
	sim = None
	with open("pl/sim") as f:
		sim =pickle.load(f)
	print "Compute psim \n"

	simp=None
	with open("pl/simp") as f:
		simp =	pickle.load(f)

	l = []
	itr = g_nt.nodes_iter()


	nodes = sorted(g_nt.nodes())
	for i in range(len(nodes)):
		if(type(nodes[i]) is  URIRef):
			print str(i) +":"+nodes[i]



	print "1 - explore node"
	print "2 - compare nodes"
	print "q - quit"
	s = raw_input("select option\n")
	nodes_list = []
	while s!="q":
		
		a = int(s)
		if a == 1:
			num = int(raw_input("select node\n"))
			explore_node(g_nt,nodes[num])
		if a == 2:
			num1 = int(raw_input("select first node\n"))
			num2 = int(raw_input("select second node\n"))
			compare_nodes(g_nt,nodes[num1],nodes[num2],sim,simp)
		s = raw_input()

