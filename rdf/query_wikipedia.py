from SPARQLWrapper import SPARQLWrapper, JSON, XML, N3, RDF, TURTLE, JSON
import logging
from rdflib import Graph,Namespace, URIRef, Literal
from rdflib.tools import rdf2dot
from rdflib.namespace import XSD
from rdflib.namespace import FOAF, RDF
from subprocess import check_call
from collections import deque
from jinja2 import Template




def buildSubQuery(template_file,name,predicate=None):
	query_template = ""

	with open(template_file,'r') as queryfile:
		query_template=Template(queryfile.read())

	if predicate != None:
		return query_template.render(name=name,predicate=predicate)
	return query_template.render(name=name)


def queryWithSparql(q,sparql):

	sparql.setQuery(q)
	sparql.setReturnFormat(JSON)
	results = []
	try:	
		results = sparql.query().convert()

	except:
		import time
		time.sleep(5)
	return results

