'''
Since graph-tool doesn't keep the order of vertices in each creation of 
the graph, we will pickle the graph after doing the calculations
'''

import gt_utils.gt_alg as galg
import gt_utils.gt_load as gload
import pickle
import os.path
import gt_utils.gt_rdf as grdf
from graph_tool import centrality

TURTLE_FILE = "graph.ttl"
LABELS_FILE = "labels"
GRAPH_FILE = "graph_pickle"
PRANK_FILE = "prank"
SIMRANK_FILE = "simerank"
GR_FILE = "gr"
BET_FILE = "betweeness"
'''
analyzes the graph and saves the results
'''
def analyze(dir_name):
	g = gload.load_graph(dir_name)
	with open(os.path.join(dir_name, GRAPH_FILE),'wb') as f:
		pickle.dump(g,f)

	sim = galg.simrank(g)
	with open(os.path.join(dir_name, SIMRANK_FILE),'wb') as f:
		pickle.dump(sim,f)

	prank = galg.psimrank(g)
	with open(os.path.join(dir_name, PRANK_FILE),'wb') as f:
		pickle.dump(prank,f)



	gr = grdf.calculate_taxonomy2(g)
	with open(os.path.join(dir_name, GR_FILE),'wb') as f:
		pickle.dump(gr,f)

	vp,ep = centrality.betweenness(analsis_dict['graph'])

	with open(os.path.join(dir_name, BET_FILE),'wb') as f:
		pickle.dump(vp,f)






'''
retreives the analysis results 
'''
def load_analysis(dir_name):
	analsis_dict={}

	with open(os.path.join(dir_name, GRAPH_FILE),'rb') as f:
		analsis_dict['graph'] = pickle.load(f)

	with open(os.path.join(dir_name,PRANK_FILE),'rb') as f:
		analsis_dict["prank"] = pickle.load(f)

	with open(os.path.join(dir_name,SIMRANK_FILE),'rb') as f:
		analsis_dict["simrank"] = pickle.load(f)

	with open(os.path.join(dir_name,GR_FILE),'rb') as f:
		analsis_dict["gr"] = pickle.load(f)

	with open(os.path.join(dir_name,BET_FILE),'rb') as f:
		analsis_dict["betweeness"] = pickle.load(f)

	return analsis_dict
			