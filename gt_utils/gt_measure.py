from __future__ import division
'''
This module defines basic calculations of semantic measures
These measures using a gr graph that is calculated in gt_rdg module

'''

import graph_tool
import gt_utils.gt_rdf as grdf
from gt_utils.constants import *

'''
return int representing the number of instances of the class of the current class node cls
'''
def get_pr(gr,clas):
	root = grdf.get_root(gr)
	return gr.vertex_properties['instances'][clas]/gr.vertex_properties['instances'][root]

'''
calculate the depth of the node 
'''
def get_depth(g,node):
	return g.vertex_properties['depth'][g.vertex_index[node]]

'''
get the lowest parents of a node
'''
def get_class(gr,node):
	for e in node.out_edges():
		if gr.edge_properties['label'][e]==rdf_type:
			return e.target()
	return node
	
'''
notice that this method is correcct only for gr graphs
'''
def get_mica(gr,u,v):
	u_parents = set()
	v_parents = set()

	while (v!=None or u!=None) and len(u_parents.intersection(v_parents))==0:
		v=gr.vertex_properties['tparent'][v]
		u=gr.vertex_properties['tparent'][u]

		u_parents.add(u)
		v_parents.add(v)


	# should atleast contain Thing
	assert u_parents.intersection(v_parents),"No common parent"
	return u_parents.intersection(v_parents).pop()

'''
notice that this method is correcct only for gr graphs
'''
def get_mica2(gr,u,v):
	u_parents = set()
	v_parents = set()

	while (v!=None or u!=None) and len(u_parents.intersection(v_parents))==0:
		v_t=None
		u_t=None

		if v!=None:
			for e in v.out_edges():
				if e.target()!=v and gr.vertex_properties['label'][e.target()]!="/Owl#Class":
					v_parents.add(e.target())
					v_t = e.target()
		if u!=None:
			for e in u.out_edges():
				if e.target()!=u and gr.vertex_properties['label'][e.target()]!="/Owl#Class":	
					u_parents.add(e.target())
					u_t = e.target()
		v = v_t
		u = u_t
	
	return u_parents.intersection(v_parents).pop()
    
