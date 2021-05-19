import networkx as nx
import collections
import pickle
import matplotlib.pyplot as plt

#REPLACE WITH THE DATA FILE YOU WANT TO USE
with open ('dataLatest.txt', 'rb') as fp:
    linked_subreddits = pickle.load(fp)


print(linked_subreddits)

G = nx.DiGraph()

for lista in linked_subreddits:
	for index, subreddit in enumerate(lista):
		if index > 0:
			spoint = str(lista[0])
			epoint = str(subreddit)
			G.add_edge(spoint, epoint)

degreeList = G.degree()
outDegreeList = G.out_degree()
inDegreeList = G.in_degree()

#creating sorted lists by degree
sortedOutDegreeList = sorted(outDegreeList, key=lambda x: x[1], reverse=True)
sortedInDegreeList = sorted(inDegreeList, key=lambda x: x[1], reverse=True)
sortedDegreeList = sorted(degreeList, key=lambda x: x[1], reverse=True)

sortedThresholdOutDegreeList = []
sortedThresholdInDegreeList = []

#make a list with a threshold of certain degree and only accept ones that are above the threshold
for i in sortedInDegreeList:
	if(i[1] > 15):
		sortedThresholdInDegreeList.append(i)

##Printing the subreddits if their degree is above a threshold
for i in sortedInDegreeList:
	if(i[1] > 10):
		print("r/" + str(i[0]) + ", " + str(i[1]))

#print(sortedThresholdOutDegreeList)
#in-degree calculations--------------------------------------------------------------
degree_sequence = sorted([d for n, d in sortedInDegreeList], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color="b")
plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
#plt.yscale('log')
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)
# draw graph in inset
plt.axes([0.4, 0.4, 0.5, 0.5])
#Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
#pos = nx.spring_layout(G)
plt.axis("off")
plt.show()

#------------------------------------------------------------------------------------