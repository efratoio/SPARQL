'''
This module contains various methods that enables drawing the graph in different manners
'''


import graph_tool.draw as gdraw



def graph_draw_out_color_square(gr,out,color):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_font_size=30,\
		edge_font_size=20,vertex_text_position=-1,\
		vertex_shape="square",\
		edge_text=gr.edge_properties['label'],output_size=(1800,1800),\
		fit_view=1,output=out,vertex_fill_color=color)
def graphviz(gr):
	gdraw.graphviz_draw(gr, pos=None, size=(15, 15), pin=False, layout=None, maxiter=None, ratio='fill', overlap=True, sep=None, splines=False, vsize=0.105, penwidth=1.0, elen=None, gprops={}, vprops={}, eprops={}, vcolor='#a40000', ecolor='#2e3436', vcmap=None, vnorm=True, ecmap=None, enorm=True, vorder=None, eorder=None, output='', output_format='auto', fork=False, return_string=False)

def graph_draw(gr):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_text_position=0.1,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1)


def graph_draw_out(gr,out):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_text_position=0.1,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1,output=out)

def graph_draw_color(gr,out,color):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_font_size=30,edge_font_size=20,vertex_text_position=2,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1,vertex_fill_color=color)

def graph_draw_out_color(gr,out,color):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_font_size=30,edge_font_size=20,vertex_text_position=2,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1,output=out,vertex_fill_color=color)

def graph_draw_closeness(gr,c):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_text_position=0.1,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1, vertex_fill_color=c)

def graph_draw_edges(gr,be):
	gdraw.graph_draw(gr,vertex_text=gr.vertex_properties['label'],vertex_text_position=0.1,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(1800,1800),fit_view=1,edge_pen_width=be)

def f_r_draw(gr):
	pos = gdraw.fruchterman_reingold_layout(gr)
	gdraw.graph_draw(gr,pos=pos,vertex_text=gr.vertex_properties['label'],vertex_text_position=0.1,vertex_size=10,edge_text=gr.edge_properties['label'],output_size=(3800,3800),fit_view=3)
