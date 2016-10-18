'''
This module loads an rdfgraph into graph-tool graph. 
It also requires a labels file, with nodes and edges labels. (that was dumped using pickle)
The turtle and pickle file shoud be in the same directory and there names must match the vaiables
TURTLE_FILE and LABLES_FILE respectively
'''

from rdflib import Graph
import rdf_graph_tool_util as rnu
import graph_tool as gt
import pickle
import os.path

TURTLE_FILE = "graph.ttl"
LABLES_FILE = "labels"

'''
loads the rdf graph from a turtle file using rdflib
'''
def load_turtle(dir_name):
	g = Graph()
	g.parse(os.path.join(dir_name,TURTLE_FILE),format="turtle")
	return g

'''
Loads labels file using pickle
'''
def load_labels(dir_name):
	with open(os.path.join(dir_name,LABLES_FILE), 'rb') as file:
		l = pickle.load(file)
	return l


'''
Converting the types, retreives graph-tool graph.
'''
def load_graph(dir_name):

	g = load_turtle(dir_name)
	l = load_labels(dir_name)

	return rnu.rdflib_to_graphtool(g,\
		transform_s=lambda s, p, o: {str('term'): s, str('label'): l[str(s.encode('utf-8'))] if str(s.encode('utf-8')) in l.keys() else s.title()[s.title().rfind("/"):]},\
		transform_p=lambda s, p, o: {str('term'): p, str('label'):l[str(p.encode('utf-8'))] if str(p.encode('utf-8')) in l.keys() else p.title()[p.title().rfind("/"):]},\
		transform_o=lambda s, p, o: {str('term'): o, str('label'):l[str(o.encode('utf-8'))] if str(o.encode('utf-8')) in l.keys() else o.title()[o.title().rfind("/"):]},)

