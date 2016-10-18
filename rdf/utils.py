from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph,URIRef
import pickle
import rdf.query_wikipedia as qw

import os.path

TURTLE_FILE = "graph.ttl"
LABLES_FILE = "labels"





def getLabels(g):

	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.timeout = 100000

	# all the rdf graph nodes
	nodes = [x for x in g.all_nodes() if type(x)==URIRef]
	labels = {}

	# all the rdf graph edges in set
	edges = set()
	for i in g.predicates():
		edges.add(i)

	for node in nodes+list(edges):
		results = []
		try:
			query = qw.buildSubQuery("rq/label.rq",str(node))
			results = qw.queryWithSparql(query,sparql)
		except:
			print "no query for "+node.encode('utf-8')
		if len(results) > 0:
			try:
				labels[str(node.encode('utf-8'))] = results['results']['bindings'][0]['c']['value'].encode('utf-8')
			except:
				print node.encode('utf-8')
		else:
			labels[str(node)] = str(node)[str(node).rfind("/"):].replace("_"," ")
			print "no label "+str(node)

	return labels



def saveLabels(dir_name):
	g = Graph()
	g.parse(os.path.join(dir_name,TURTLE_FILE),format="turtle")

	labels = getLabels(g)
	with open(os.path.join(dir_name,LABLES_FILE),"w") as f:
		pickle.dump(labels,f)



