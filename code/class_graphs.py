# -*- coding: utf-8 -*-

import math

"""
graph = {pred1: {succ11: weight11, succ12: weight12}
		 pred2: {succ21: weight21, succ22: weight22}
		 pred3: {succ31: weight31, succ32: weight32}}
"""

class Graph:

	def __init__(self, graph = {}) -> None:
		"""
		Inicializa uma instância da classe Graph, guardando um grafo introduzido pelo utilizador. Caso não 
		seja introduzido qualquer grafo, self.graph é inicializado como um dicionário vazio.

		Parameters
		----------
		:param graph: O grafo introduzido pelo utilizador
		"""
		self.graph = graph

	def __str__(self) -> str:
		"""
		Imprime o grafo (na forma de dicionário).
		"""
		return str(self.graph)


	########## NODOS, ARCOS E TAMANHO DO GRAFO ##########

	def print_graph(self) -> None:
		"""
		Imprime, de forma legível, todas as relações entre nodos do grafo.
		"""
		for node in self.graph:
			for k in self.graph[node]:
				print(f"{node} ---({self.graph[node][k]})---> {k}")

	def get_nodes(self) -> list:
		"""
		Retorna uma lista contendo todos os nodos do grafo.
		"""
		return self.graph.keys()

	def get_edges(self) -> list:
		"""
		Retorna uma lista contendo todos os arcos do grafo.
		"""
		return [(k, v) for k in self.graph for v in self.graph[k]]

	def size(self):
		"""
		Retorna o número de nodos e arcos do grafo.
		"""
		return len(self.get_nodes()), len(self.get_edges())


	########## ADICIONAR NODOS E ARCOS AO GRAFO ##########

	def add_node(self, node: int) -> None:
		"""
		Adiciona um novo nodo ao grafo.

		Parameters
		----------
		:param node: Nodo a introduzir no grafo

		"""
		if node not in self.graph:
			self.graph[node] = {}

	def add_edge(self, fr: int, to: int, weight: int) -> None:
		"""
		Adiciona um novo arco ao grafo.

		Parameters
		----------
		:param fr: O nodo de origem
		:param to: O nodo de destino
		:param weight: O peso da ligação entre "fr" e "to"
		"""
		self.add_node(fr)
		self.add_node(to)
		self.graph[fr][to] = weight


	########## NODOS SUCESSORES, PREDECESSORES E ADJACENTES ##########

	def get_successors(self, node: int) -> list:
		"""
		Retorna uma lista contendo os sucessores do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujos sucessores se pretende determinar
		"""
		return [s for s in self.graph[node]]

	def get_predecessors(self, node: int) -> list:
		"""
		Retorna uma lista contendo os nodos predecessores do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujos predecessores se pretende determinar
		"""
		return [p for p in self.graph if node in self.graph[p]]

	def get_adjacents(self, node: int) -> list:
		"""
		Retorna uma lista contendo os nodos adjacentes ao nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujos nodos adjacentes se pretende determinar
		"""
		s = self.get_successors(node)
		p = self.get_predecessors(node)
		return list(set(s + p))


	########## GRAUS DOS NODOS DO GRAFO ##########

	def out_degree(self, node: int) -> int:
		"""
		Retorna o grau de saída do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujo grau de saída se pretende determinar
		"""
		return len(self.get_successors(node))

	def in_degree(self, node: int) -> int:
		"""
		Retorna o grau de entrada do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujo grau de entrada se pretende determinar
		"""
		return len(self.get_predecessors(node))

	def degree(self, node: int) -> int:
		"""
		Retorna o grau do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujo grau se pretende determinar
		"""
		return len(self.get_adjacents(node))

	def all_degrees(self, deg_type: str = "inout") -> dict:
		"""
		Retorna um dicionário cujas chaves são todos os nodos do grafo e os valores são os seus graus.

		Parameters
		----------
		:param type: O tipo de grau que se pretende determinar. Toma os valores "out" (grau de saída), "in" 
		(grau de entrada) ou "inout" (grau "total")
		"""
		
		msg = "O parâmetro deg_type apenas toma os valores 'in', 'out' ou 'inout'."
		assert deg_type in ["in", "out", "inout"], msg
		
		if deg_type == "out": func = self.out_degree
		elif deg_type == "in": func = self.in_degree
		else: func = self.degree

		return {node: func(node) for node in self.get_nodes()}


	########## NODOS ATINGÍVEIS COM OS MÉTODOS BFS E DFS ##########

	# BFS: Queue (FIFO -> first in, first out)
	def reachable_bfs(self, fr: int) -> list:
		"""
		Retorna uma lista contendo todos os nodos atingíveis pelo nodo de origem (implementa o método 
		breadth-first search).

		Parameters
		----------
		:param fr: O nodo de origem
		"""
		l = [fr]
		res = []
		while len(l) > 0:
			node = l.pop(0)
			if node != fr: res.append(node)
			for elem in self.graph[node]:
				if elem not in res and elem not in l:
					l.append(elem)
		return res

	"""
	ALTERNATIVA BFS (SEM QUEUE) -> adaptar para a classe Graph !!!

	# retorna os nodos sucessores do nodo atual
	def successors(graph, node):
		return [k for k in graph[node].keys()]

	# adiciona um novo nodo ao set de nodos visitados
	def new_visited(visited, level):
		return set(level).union(visited) # visited

	# procura um nodo alvo (target) a partir do nodo atual (current) num grafo orientado
	# para a procura num grafo não orientado, mudar "successors" para "adjacents"
	def breadth_first(graph, current, target):
		levels, visited = [[current]], {current}
		i = 0
		# termina quando todos os nodos de levels[i-1] são "folhas" 
		while levels[i]:
			levels += [[]]
			for s in levels[i]:
				levels[i+1] += successors(graph, s)
				if target in levels[i+1]: return f"FOUND {target} at level {i+1}", levels
			# termina quando todos os nodos de levels[i+1] já foram visitados
			if set(levels[i+1]).issubset(visited): break
			visited = new_visited(visited, levels[i+1])
			i += 1
		return f"{target} NOT FOUND (searched {i} levels)", levels
	"""

	# DFS: Stack (LIFO -> last in, first out)
	def reachable_dfs(self, fr: int) -> list:
		"""
		Retorna uma lista contendo todos os nodos atingíveis pelo nodo de origem (implementa o método 
		depth-first search).

		Parameters
		----------
		:param fr: O nodo de origem
		"""
		l = [fr]
		res = []
		while len(l) > 0:
			node = l.pop(0)
			if node != fr: res.append(node)
			s = 0
			for elem in self.graph[node]:
				if elem not in res and elem not in l:
					l.insert(s, elem)
					s += 1
		return res


	########## NODOS ATINGÍVEIS COM DISTÂNCIAS (BASEADO NO MÉTODO BFS) ##########

	def __is_in_tuple_list(self, tuple_list: list, node: int) -> bool:
	    """
	    Método auxiliar de reachable_with_dist() que retorna True ou False dependendo de o nodo (que toma 
	    como parâmetro) se encontrar na lista de tuplos ou não.

	    Parameters
		----------
		:param tuple_list: A lista de tuplos
		:param node: O nodo a procurar na lista de tuplos
	    """
	    for (x, y) in tuple_list:
	        if node == x: return True
	    return False

	def reachable_with_dist(self, fr: int) -> list:
		"""
		Retorna uma lista de tuplos contendo um nodo de destino e a sua distância à origem (implementado com 
		base no método breadth-first search).
		
		Parameters
		----------
		:param fr: O nodo de origem
		"""
		res = []
		l = [(fr, 0)]
		while len(l) > 0:
		    node, dist = l.pop(0)
		    if node != fr: res.append((node, dist))
		    for elem in self.graph[node]:
		        if not self.__is_in_tuple_list(l, elem) and not self.__is_in_tuple_list(res, elem): 
		            l.append((elem, dist+1))
		return res


	########## DIJKSTRA ##########

	def __get_mins(self, distances: dict) -> tuple:
		"""
		Método auxiliar de dijkstra() que retorna um tuplo com os valores da menor distância ao nodo de origem e os 
		nodos para os quais esta se verifica.

		Parameters
		----------
		:param distances: O dicionário de distâncias
		"""
		min_dist = math.inf
		prev_node = min_node = None
		for node in distances:
			for k in distances[node]:
				if distances[node][k] < min_dist:
					prev_node = node
					min_node = k
					min_dist = distances[node][k]
		return prev_node, min_node, min_dist

	def __get_path(self, djkstr: dict, fr: int, to: int) -> str:
		"""
		Método auxiliar de dijkstra() que retorna o caminho mais curto entre o nodo de origem e o nodo de destino
		de forma legível.

		Parameters
		----------
		:param djkstr: O dicionário de distâncias
		:param fr: O nodo de origem
		:param to: O nodo de destino
		"""
		node = to
		path = [str(node)]
		while node != fr:
			node = djkstr[node][0]
			path.insert(0, str(node))
		return " -> ".join(path) + f" (dist = {djkstr[to][1]})"

	def dijkstra(self, fr: int, to: int) -> str:
		"""
		Implementação do algoritmo de Dijkstra. Caso exista, retorna o caminho mais curto entre um nodo de origem e um 
		nodo de destino. Caso contrário, retorna uma mensagem de erro.

		Parameters
		----------
		:param fr: O nodo de origem
		:param to: O nodo de destino
		"""
		djkstr = {k: [0, 0] for k in self.graph} # djkstr[k][0] -> proveniência; djkstr[k][1] -> distância ao nodo inicial
		marked = [fr]
		while to not in marked:
			distances = {}
			for node in marked:
				distances[node] = {}
				for k in self.graph[node]:
					if k not in marked: # de modo a não incluír como destino nodos já marcados no dicionário de distâncias
						distances[node][k] = self.graph[node][k] + djkstr[node][1]
			prev_node, min_node, min_dist = self.__get_mins(distances)
			if min_node is None: return f"ERRO: Não existe qualquer caminho entre {fr} e {to}!"
			marked += [min_node]
			djkstr[min_node][0] = prev_node
			djkstr[min_node][1] = min_dist
		return self.__get_path(djkstr, fr, to) # alterar ???


	########## CICLOS ##########

	def node_has_cycle(self, n: int) -> bool:
		"""
		Identifica a presença de um ciclo para um determinado nodo do grafo (baseado no método BFS).

		Parameters
		----------
		:param n: O nodo para o qual se pretende verificar a existência de um ciclo
		"""
		l = [n]
		visited = [n]
		while len(l) > 0:
		    node = l.pop(0)
		    for elem in self.graph[node]:
		        if elem == n: return True
		        elif elem not in visited:
		            l.append(elem)
		            visited.append(elem)
		return False

	def has_cycle(self) -> bool:
		"""
		Verifica se existe pelo menos um ciclo no grafo.
		"""
		for node in self.graph:
		    if self.node_has_cycle(node): return True
		return False


	########## MÉTRICAS EM GRAFOS ##########

	def mean_degree(self, deg_type: str = "inout") -> float:
		"""
		Retorna o grau médio dos nodos do grafo dependendo do tipo de grau ('out', 'in', 'inout').

		Parameters
		----------
		:param deg_type: O tipo de grau
		"""
		degs = self.all_degrees(deg_type)
		return sum(degs.values()) / len(degs)
	
	def prob_degree(self, deg_type: str = "inout") -> list:
		"""
		Retorna a probabilidade de ocorrência de cada grau no grafo dependendo do tipo de grau

		Parameters
		----------
		:param deg_type: O tipo de grau ('out', 'in', 'inout')
		"""
		degs = self.all_degrees(deg_type)
		res = {}
		for k in degs:
			if degs[k] in res: res[degs[k]] += 1
			else: res[degs[k]] = 1
		return sorted((k, float(f"{res[k]/len(degs):.2f}")) for k in res)

	def mean_distances(self):
		"""
		Retorna a distância média entre nodos do grafo.
		"""
		total = 0
		num_reachable = 0
		for k in self.graph:
			dists = self.reachable_with_dist(k)
			for node, dist in dists: # node -> nodo atingível; dist -> distância a esse nodo
				total += dist
			num_reachable += len(dists) # += número de nodos atingíveis pelo nodo k
		meandist = total / num_reachable
		return meandist

	def clustering_coef(self, node: int) -> float:
		"""
		Retorna o coeficiente de clustering para um dado nodo do grafo.

		Parameters
		----------
		:param node: O nodo para o qual se pretende calcular o coeficiente de clustering
		"""
		adjs = self.get_adjacents(node)
		if len(adjs) <= 1: return 0.0
		ligs = 0
		for i in adjs:
			for j in adjs:
				if i != j:
					if j in self.graph[i] or i in self.graph[j]: ligs += 1
		return ligs / (len(adjs) * (len(adjs)-1))

	def all_clustering_coefs(self) -> dict:
		"""
		Retorna os coeficientes de clustering de todos os nodos do grafo na forma de dicionário.
		"""
		return {k: self.clustering_coef(k) for k in self.graph}

	def mean_clustering_coef(self) -> float:
		"""
		Retorna o coeficiente de clustering médio.
		"""
		ccs = self.all_clustering_coefs()
		return sum(ccs.values()) / len(ccs)

	def mean_clustering_per_degree(self, deg_type: str = "inout") -> dict:
		"""
		Retorna um dicionário em que as keys são os graus existentes no grafo e os values são a média dos coeficientes
		de clustering dos nodos que têm esse grau.

		Parameters
		----------
		:param deg_type: O tipo de grau ('out', 'in', 'inout')
		"""
		degs = self.all_degrees(deg_type)
		ccs = self.all_clustering_coefs()
		degs_k = {} # dicionário em que as keys são os graus e os values são os nodos que têm esse grau
		for k in degs:
			if degs[k] in degs_k: degs_k[degs[k]] += [k]
			else: degs_k[degs[k]] = [k]
		cc_per_k = {} # dicionário em que as keys são os graus e os values são a média dos cc dos nodos com esse grau
		for k in degs_k:
			total = 0
			for node in degs_k[k]: total += ccs[node] # para cada nodo de grau k adicionar o seu cc ao total
			cc_per_k[k] = total / len(degs_k[k]) # média dos coeficentes de clustring dos nodos de grau k
		return cc_per_k

	#### ADICIONAR AS RESTANTES MÉTRICAS !!! ####


if __name__ == "__main__":

	gr = Graph( {1:{2:2, 3:5}, 2:{1:2, 3:3, 4:1, 5:2}, 3:{1:5, 2:3, 4:1, 5:2},
                   4:{2:1, 3:1, 5:2, 6:7}, 5:{2:2, 3:2, 4:2, 6:3}, 6:{4:7, 5:3}} )
	print(gr.dijkstra(1,6))

	# Inicializar grafo e adicionar arcos
	g = Graph()
	edges = [(1,5,7), (1,2,2), (2,3,8), (2,4,1), (3,8,5), (3,9,5), (4,7,4), (7,10,4), (9,1,6), (9,10,2), (11,12,1)]
	for edge in edges:
		g.add_edge(*edge)

	print("Ligações presentes no grafo e respetivos pesos")
	g.print_graph()

	print("\nTamanho do grafo")
	s = g.size()
	print(f"Nodos: {s[0]}, Arcos: {s[1]}\n")

	print("Sucessores (de 1), predecessores (de 10) e adjacentes (de 1)")
	print(g.get_successors(1), g.get_predecessors(10), g.get_adjacents(1))

	print("\nGraus de saída (de 1), de entrada (de 10) e total (de 1)")
	print(g.out_degree(1), g.in_degree(10), g.degree(1))

	print("\nGraus (total) de todos os nodos do grafo")
	print(g.all_degrees("inout"))

	print("\nNodos atingíveis (de 1) -> métodos BFS e DFS, respetivamente")
	print(g.reachable_bfs(1))
	print(g.reachable_dfs(1))

	print("\nNodos atingíveis (de 1) com distâncias -> baseado no método BFS")
	print(g.reachable_with_dist(1))

	print("\nCaminho mais curto entre 1 e 10 (algoritmo de Dijkstra)")
	print(g.dijkstra(1, 10))
	print(g.dijkstra(1, 12))

	print("\nVerificar a presença de ciclos no grafo")
	print("Nodo 1:", g.node_has_cycle(1))
	print("Nodo 10:", g.node_has_cycle(10))
	print("Grafo:", g.has_cycle())

	print("\nMétricas")
	print(f"Grau médio (deg_type == 'inout'): {g.mean_degree()}")
	print(f"Probabilidade de cada grau (deg_type == 'inout'): {g.prob_degree()}")
	print(f"Distância média entre nodos: {g.mean_distances():.2f}")
	print(f"Coeficiente de clustering (nodo 1): {g.clustering_coef(1)}") # ???
	print(f"Coeficientes de clustering: {g.all_clustering_coefs()}") # ???
	print(f"Média dos coeficientes de clustering: {g.mean_clustering_coef()}")
	print(f"Média dos coeficientes de clustering por grau: {g.mean_clustering_per_degree()}")
