import matplotlib.pyplot as plt
import networkx as nx
import pickle
import collections


with open ('data.txt', 'rb') as fp:
    linked_subreddits = pickle.load(fp)
"""
hd = "H" + chr(252) + "sker D" + chr(252)
mh = "Mot" + chr(246) + "rhead"
mc = "M" + chr(246) + "tley Cr" + chr(252) + "e"
st = "Sp" + chr(305) + "n" + chr(776) + "al Tap"
q = "Queensr" + chr(255) + "che"
boc = "Blue " + chr(214) + "yster Cult"
dt = "Deatht" + chr(246) + "ngue"

G = nx.DiGraph()
G.add_edge(hd, mh)
G.add_edge(mc, st)
G.add_edge(boc, mc)
G.add_edge(boc, dt)
G.add_edge(st, dt)
G.add_edge(q, st)
G.add_edge(dt, mh)
G.add_edge(st, mh)
"""
labels = {}

G = nx.Graph()
node_list = []
for lista in linked_subreddits:
	for index, subreddit in enumerate(lista):
		if index > 0:
			spoint = str(lista[0])
			epoint = str(subreddit)
			G.add_edge(spoint, epoint)

for i in G.nodes():
	#print(G.degree[i])
	if G.degree[i] > 15:
		labels[i] = i


print(list(G.nodes()))

d = dict(G.degree)

#Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(G)

nx.draw(G, pos, font_size=16, with_labels=False, edge_color='gray', width=0.5, node_size=[v * 10 for v in d.values()])
nx.draw_networkx_labels(G,pos,labels,font_size=16,font_color='r')
#nx.draw_networkx_edges(G, pos, alpha=0.4)
plt.show()


#for i in G.nodes():
	#print(G.degree[i])
#	if G.degree[i] > 1:
#		node_list.append(i)
#print(node_list)
#G.remove_edges_from(list(G.edges))
#nx.draw_random(G, font_size=16, with_labels=True, edge_color='gray', width=0.5, node_size=[v * 100 for v in d.values()])
#for p in pos:  # raise text positions
#    pos[p][1] += 0.07
#nx.draw_networkx_labels(G, pos)
#plt.show()
