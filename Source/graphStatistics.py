from graph_tool.all import *
import numpy as np
import matplotlib.pyplot as plt
import os

def create_hist(x, x_title, y_title, path, title, is_ready=False):
	if is_ready:
		myX = x
	else:
		myX = []
		for i, x in enumerate(x):
			aux = [i]*int(x)
			myX+=aux
	myY = np.arange(max(myX)+2)

	plt.figure(figsize=(6,4))
	plt.title(title)
	plt.gca().hist(myX, myY, normed=1, facecolor='blue', alpha=0.7, rwidth=0.9, align='left')
	plt.xlabel(x_title)
	plt.ylabel(y_title)
	plt.tight_layout()
	plt.savefig(path)

def create_plot(y, x_title, y_title, path, title):
	x = np.arange(len(y))
	plt.figure(figsize=(6,4))
	plt.title(title)
	plt.gca().plot(x, y, color='blue', alpha=0.7, linestyle='None', marker='o')
	plt.xlabel(x_title)
	plt.ylabel(y_title)
	plt.tight_layout()
	plt.savefig(path)

def my_pct(values):
	def my_autopct(pct):
		if pct > 1:
			return '{p:.1f}%'.format(p=pct)
		else:
			return ''     
	return my_autopct

if __name__ == '__main__':
	# {Graph path: graph type}
	graphsInfo = {
		"/Users/admin/Documents/UFRJ/RedesComplexas_ProjetoFinal/BooksNetworks/HP_book1.gml": ["weighted", "undirected"]
	}

	for graphPath, graphType in graphsInfo.items():
		graphDir = graphPath.replace(graphPath.split('/')[-1], '')
		graphName = graphPath.split('/')[-1]
		print('\n{:<15}: {}'.format('Graph', graphName))
		g = load_graph(graphPath)

		# Qnt de nos e arestas
		edges = g.get_edges()
		vertices = g.get_vertices()
		print ('{:<15}: {:^8}, {:<8}: {:^8}'.format('Arestas', len(edges), 'Vertices', len(vertices)))

		weight = None
		if "weighted" in graphType:
			weight = g.edge_properties['weight']
		directed = False
		if "directed" in graphType:
			directed = True


		# Grau Medio				
		grau_medio, dp_grau_medio = graph_tool.stats.vertex_average(g, 'total')
		grau_medio_in, dp_grau_medio_in = graph_tool.stats.vertex_average(g, 'in')
		grau_medio_out, dp_grau_medio_out = graph_tool.stats.vertex_average(g, 'out')
		# Inicializando com um valor existente no grafo
		grau_max = g.vertex(0).in_degree() + g.vertex(0).out_degree()
		grau_min = g.vertex(0).in_degree() + g.vertex(0).out_degree()
		grau_in_max = g.vertex(0).in_degree()
		grau_in_min = g.vertex(0).in_degree()
		grau_out_min = g.vertex(0).out_degree()
		grau_out_max = g.vertex(0).out_degree()
		for v in vertices:
			g_in    = g.vertex(v).in_degree()
			g_out   = g.vertex(v).out_degree()
			g_total = g_in+g_out
			if g_in  < grau_in_min: grau_in_min   = g_in
			if g_in  > grau_in_max: grau_in_max   = g_in
			if g_out < grau_out_min: grau_out_min = g_out
			if g_out > grau_out_max: grau_out_max = g_out
			if g_total > grau_max : grau_max = g_total
			if g_total < grau_min : grau_min = g_total
		print('{:<15} -> {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<3}: {:^8.3f}'.format('Grau total', 
						'Maximo', grau_max, 'minimo', grau_min, 'media', grau_medio, 'dp', dp_grau_medio))

		# Grau total hist
		grau_hist = graph_tool.stats.vertex_hist(g, 'total')
		create_hist(grau_hist[0], "$Grau_{k}$", "PDF P[D=k]", graphDir+"deg-dist.png", "Distribuicao do grau total para "+graphName)

		# Betwenness
		vb_map, eb_map = graph_tool.centrality.betweenness(g, weight=weight)
		vb_max = max(vb_map.a)
		vb_min = min(vb_map.a)
		vb_media, dp_vb = graph_tool.stats.vertex_average(g, vb_map)
		print('{:<15} -> {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<3}: {:^8.3f}'.format('Betwenness', 
							'Maximo', vb_max, 'minimo', vb_min, 'media', vb_media, 'dp', dp_vb))
		create_plot(vb_map.a, "$Grau_{k}$", "$Betwenness_{k}$", graphDir+"betweenness-dist.png", "Distribuicao do betweenness para "+graphName)

		# Katz
		katz_map = graph_tool.centrality.katz(g, weight=weight)
		katz_max = max(katz_map.a)
		katz_min = min(katz_map.a)
		katz_media, dp_katz = graph_tool.stats.vertex_average(g, katz_map)
		print('{:<15} -> {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<3}: {:^8.3f}'.format('Katz', 
							'Maximo', katz_max, 'minimo', katz_min, 'media', katz_media, 'dp', dp_katz))
		create_plot(katz_map.a, "$Grau_{k}$", "$Katz_{k}$", graphDir+"katz-dist.png", "Distribuicao de katz para "+graphName)

		# Pagerank
		pagerank_map = graph_tool.centrality.pagerank(g, weight=weight)
		pagerank_max = max(pagerank_map.a)
		pagerank_min = min(pagerank_map.a)
		pagerank_media, dp_pagerank = graph_tool.stats.vertex_average(g, pagerank_map)
		print('{:<15} -> {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<3}: {:^8.3f}'.format('Pagerank', 
							'Maximo', pagerank_max, 'minimo', pagerank_min, 'media', pagerank_media, 'dp', dp_pagerank))
		create_plot(pagerank_map.a, "$Grau_{k}$", "$Pagerank_{k}$", graphDir+"pagerank-dist.png", "Distribuicao do pagerank para "+graphName)

		# Clusterizacao local
		clust = graph_tool.clustering.local_clustering(g, undirected=(not directed))
		clust_max = max(clust.a)
		clust_min = min(clust.a)
		clust_media, dp_clust = graph_tool.stats.vertex_average(g, clust)
		print('{:<15} -> {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<8}: {:^8.3f} | {:<3}: {:^8.3f}'.format('Clust. local', 
							'Maximo', clust_max, 'minimo', clust_min, 'media', clust_media, 'dp', dp_clust))
		create_plot(clust.a, "$Grau_{k}$", "$Clusterizacao_{k}$", graphDir+"clust-dist.png", 
							"Distribuicao da clusterizacao local para "+graphName)

		# Clusterizacao global
		global_clust, dp_global_clust = graph_tool.clustering.global_clustering(g)
		print('{:<15}: {:^8.3f}, {:<3}: {:^8.3f}'.format('Clust. global', global_clust, 'dp', dp_global_clust))

		# Componentes
		comp, hist = graph_tool.topology.label_components(g, directed=directed)
		number_of_components = len(np.unique(comp.a))
		bigger_component = hist[np.unique(np.where(hist==max(hist)))]
		print('{:<15} {:^8}, {:<8}: {:^8}'.format('Conected comp.:', number_of_components, 'bigger', int(bigger_component)))
		if number_of_components > 1:
			x = comp.a
			sizes = hist
			labels = [str(i) for i in range(len(sizes))]

			plt.figure(figsize=(6,4))
			plt.title('Tamanho das componentes conexas de '+graphName)
			plt.gca().pie(sizes, autopct=my_pct(sizes), shadow=True, startangle=90)
			plt.gca().axis('equal')
			plt.savefig(graphDir+"conected-components.png")

		pos = graph_tool.draw.sfdp_layout(g, groups=comp, eweight=weight)
		graph_tool.draw.graph_draw(g, pos=pos, vertex_text=g.vertex_index, output=graphDir+"graph-draw-sfdp.png")
		pos = graph_tool.draw.arf_layout(g, max_iter=0)
		graph_tool.draw.graph_draw(g, pos=pos, vertex_text=g.vertex_index, output=graphDir+"graph-draw-arf.png")



