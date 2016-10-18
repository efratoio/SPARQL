'''
This module helps to enforce ontology methodology  on graph-tool graphs. 
It contains method that add semantic functionality to the graph-tool
'''
import graph_tool
from collections import deque
from gt_utils.constants import *


'''
get the root of taxonomy
'''
def get_root(g):
	for v in g.vertices():

		if g.vertex_properties['label'][v] == root_label:
			return v


def help_print(gt):
	for e in gt.edges():
		print "s: "+gt.vertex_properties['label'][e.source()] +\
		" : "+"d: "+gt.vertex_properties['label'][e.target()]


def rec_sum_calc(gr,node):
	if gr.vertex_properties['instances'][node] > 0:
		return gr.vertex_properties['instances'][node]

	gr.vertex_properties['instances'][node] = \
	sum([rec_sum_calc(gr,n) for n in node.in_neighbours()])
	
	return gr.vertex_properties['instances'][node]




'''
this method creates a taxonomy + instances tree.
'''
def calculate_taxonomy2(g):

	#remove edged different then 'subclass'
	gt = graph_tool.GraphView(g,efilt=lambda e: \
	 g.edge_properties['label'][e.source(),e.target()] == rdf_subclass\
	 or g.edge_properties['label'][e.source(),e.target()] == rdf_type)


	#remove vertices with zero out edges that are not the root
	gt = graph_tool.GraphView(gt,vfilt=lambda v: v.out_degree()> 0 \
		or gt.vertex_properties['label'][gt.vertex_index[v]] == root_label)


	#finding the depth of each concept/instance
	root = get_root(gt)

	q = deque([99999])
	q.append(root)
	i=0
	elements={root :i}
	
	while q:
		v = q.popleft()

		if v ==99999 :
			if q:
				i+=1
				q.append(99999)
		else:
			 for n in v.in_neighbours():
				q.append(n)
				elements[n] = i;



	#property map to filter superfluous edges
	p_map = g.new_edge_property("bool",val=False)
	g.vertex_properties['depth'] = g.new_vertex_property("int")
	g.vertex_properties['tparent'] = g.new_vertex_property("int",val=g.vertex_index[root])
	g.vertex_properties['class'] = g.new_vertex_property("bool")
	g.vertex_properties['instances'] = g.new_vertex_property("int",val=1)

	g.vertex_properties['instances'][root] = 0
	q = deque([99999])
	q.append(root)
	i=0

	while q:
		v = q.popleft()
		if v ==99999 :
			if q:
				i+=1
				q.append(99999)
		else:
			 for n in v.in_neighbours():

				if i == elements[n]:
					q.append(n)
					p_map[gt.vertex_index[n],gt.vertex_index[v]] = True
					g.vertex_properties['depth'][gt.vertex_index[n]] = i
					g.vertex_properties['tparent'][gt.vertex_index[n]] = gt.vertex_index[v]
					if g.edge_properties['label'][n,v] == rdf_subclass:
						g.vertex_properties['class'][gt.vertex_index[n]] = True
						g.vertex_properties['instances'][gt.vertex_index[n]] =0

				
	rec_sum_calc(g,root)
	gt = graph_tool.GraphView(g,efilt=lambda e: p_map[e.source(),e.target()])
	gt = graph_tool.GraphView(gt,vfilt=lambda v: v.out_degree()> 0 \
		or gt.vertex_properties['label'][gt.vertex_index[v]] == root_label)
	return gt


# deprecated
# '''
# this method creates a taxonomy + instances tree.
# '''
# def calculate_taxonomy(g):

# 	#remove edged different then 'subclass'
# 	gt = graph_tool.GraphView(g,efilt=lambda e: \
# 	 g.edge_properties['label'][e.source(),e.target()] == rdf_subclass)


# 	#remove vertices with not out edges that are not the root
# 	gt = graph_tool.GraphView(gt,vfilt=lambda v: v.out_degree()> 0 \
# 		or gt.vertex_properties['label'][gt.vertex_index[v]] == root_label)


# 	#finding the depth of each concept
# 	root = get_root(gt)

# 	q = deque([0])
# 	q.append(root)
# 	i=0
# 	elements={root :i}
	
# 	while q:
# 		v = q.popleft()

# 		if v ==0 :
# 			if q:
# 				i+=1
# 				q.append(0)
# 		else:
# 			 for n in v.in_neighbours():
# 				q.append(n)
# 				elements[n] = i;



# 	#property map to filter superfluous edges
# 	p_map = g.new_edge_property("bool",val=False)
# 	g.vertex_properties['depth'] = g.new_vertex_property("int")
# 	q = deque([0])
# 	q.append(root)
# 	i=0

# 	while q:
# 		v = q.popleft()
# 		if v ==0 :
# 			if q:
# 				i+=1
# 				q.append(0)
# 		else:
# 			 for n in v.in_neighbours():
# 				if i == elements[n]:
# 					q.append(n)
# 					p_map[gt.vertex_index[n],gt.vertex_index[v]] = True
# 					g.vertex_properties['depth'][gt.vertex_index[n]] = i
				

# 	gt = graph_tool.GraphView(g,efilt=lambda e: p_map[e.source(),e.target()])
# 	gt = graph_tool.GraphView(gt,vfilt=lambda v: v.out_degree()> 0 \
# 		or gt.vertex_properties['label'][gt.vertex_index[v]] == root_label)
# 	return gt



# def rec_sum_calc(gr,node):
# 	if gr.vertex_properties['instances'][node] > 0:
# 		return gr.vertex_properties['instances'][node]

# 	gr.vertex_properties['instances'][node] = sum([rec_sum_calc(gr,n) for n in node.in_neighbours()])
# 	return gr.vertex_properties['instances'][node]






# '''
# calculate a graph conatining taxonomy and instances
# return the depth of each class and the number of instances for each
# class
# '''
# def calculate_instances(g,gt):
# 	#remove edged different then "type" or 'subclass'
# 	gr = graph_tool.GraphView(g,efilt=lambda e: \
# 		g.edge_properties['label'][e.source(),e.target()] == rdf_type)

# 	gr = graph_tool.GraphView(g,vfilt=lambda v: v.in_degree()+v.out_degree()>0)


# 	edge_filt = gt.get_edge_filter()[0]

# 	g.vertex_properties['instances'] = g.new_vertex_property('int',val=0)

# 	#find the maximal parent
# 	for v in gr.vertices():
# 		mx = 0
# 		mx_arg = None
# 		#only instances will match
# 		if v.out_degree()>1:
# 			for n in v.out_neighbours():
# 				if gr.vertex_properties['depth'][n] > mx:
# 					mx = gr.vertex_properties['depth'][n]
# 					mx_arg = n
# 			if mx > 0 :
# 				edge_filt[g.edge(v,mx_arg)] = True
# 				g.vertex_properties['instances'][mx_arg] += 1 
# 		#else there is only 1 neighbour
# 		else:
# 			for n in v.out_neighbours():
# 				edge_filt[g.edge(v,n)] = True
# 				g.vertex_properties['instances'][n] += 1 

# 	# finish instances calculation
# 	root = get_root(g)
# 	rec_sum_calc(g,root)
# 	gr = graph_tool.GraphView(g,efilt=edge_filt)

# 	return gr



			









