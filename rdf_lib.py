import rdflib

graph = rdflib.Graph()
graph.parse("yagoFactsSubset.ttl", format='n3')

print(len(graph)) # graph length

# for s,p,o in graph.triples( (None, None, None) ):
#    print(s,p,o)