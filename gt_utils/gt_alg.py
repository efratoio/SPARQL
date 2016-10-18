'''
This modules conains the complicated algorithms that that calculates semantic measures
'''


import math
import numpy, itertools

import gt_utils.gt_rdf as grdf
import gt_utils.gt_measure as gmeasure

def psimrank(G, r=0.8, max_iter=100, eps=1e-4,lamda=0.6):


    sim_prev = numpy.zeros(G.num_vertices())
    sim = numpy.identity(G.num_vertices())

    adjacency_lists={}
    for u in G.vertices():
        adjacency_lists[G.vertex_index[u]]=([G.vertex_index[x] for x in G.vertex(u).in_neighbours()], \
        [G.vertex_index[x] for x in G.vertex(u).out_neighbours()])

    for i in range(max_iter):
        if numpy.allclose(sim, sim_prev, atol=eps):
            break
        sim_prev = numpy.copy(sim)
        for u, v in itertools.product(range(G.num_vertices()), range(G.num_vertices())):
            if u is v:
                continue
            u_ins, v_ins = adjacency_lists[u][0] , adjacency_lists[v][0] 
            u_ons, v_ons = adjacency_lists[u][1] , adjacency_lists[v][1] 
            # evaluating the similarity of current iteration nodes pair
            if len(u_ins)+len(u_ons) == 0 or len(v_ins)+len(v_ons) == 0: 
                # if a node has no predecessors then setting similarity to zero
                sim[u][v] = 0
            else:                    
                s_uv = lamda*sum([sim_prev[u_n][v_n] for u_n, v_n in itertools.product(u_ins, v_ins)]) \
                + (1-lamda)*sum([sim_prev[u_n][v_n] for u_n, v_n in itertools.product(u_ons, v_ons)])
                sim[u][v] = (r * s_uv) / ((len(u_ins)+len(u_ons)) * (len(v_ins)+len(v_ons)))


    return sim


def simrank(G, r=0.8, max_iter=100, eps=1e-4):
    return psimrank(G,r,max_iter,eps,1)




def simresnik(gr,u,v):
    mica = gmeasure.get_mica(gr,u,v)
    
    pr_mica = gmeasure.get_pr(gr,mica)
    return -math.log(pr_mica)

def simlin(gr,u,v):
    mica = gmeasure.get_mica(gr,u,v)
    u_class = gmeasure.get_class(gr,u)
    v_class = gmeasure.get_class(gr,v)

    pr_mica = gmeasure.get_pr(gr,mica)
    pr_u_class = gmeasure.get_pr(gr,u_class)
    pr_v_class = gmeasure.get_pr(gr,v_class)

    IC_mica = -math.log(pr_mica)
    IC_u_class = -math.log(pr_u_class)
    IC_v_class = -math.log(pr_v_class)

    return (2*IC_mica)/(IC_u_class+IC_v_class)