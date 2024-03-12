import networkx as nx


G = nx.Graph()
with open("data/yeast/BioGRID.txt", 'r') as file:
    for line in file:
        line = line.strip()
        nodes = line.split("\t")
        G.add_edge(nodes[0], nodes[1])

labels = []
with open("data/yeast/disprotYeast194.txt", 'r') as file:
    for line in file:
        line = line.strip()
        labels.append(line)

print(G)
print(labels)

for node in list(G.nodes()):
    if G.degree(node) == 1:
        G.remove_node(node)
        if node in labels:
            labels.remove(node)
print(G)

for node in list(G.nodes()):
    if G.degree(node) == 1:
        G.remove_node(node)
        if node in labels:
            labels.remove(node)

counter1 = 0
counter2 = 0
for i in G.nodes:
    if len(G[i]) == 1:
        counter1 += 1
        if i in labels:
            counter2 += 1

print(counter1, counter2)

file_path = "data/yeast/BioGRID_withoutLeaves.txt"
nx.write_edgelist(G, file_path)
with open("data/yeast/disprotYeast194_withoutLeaves.txt", 'w') as file:
    # Iteriranje kroz svaki element liste
    for element in labels[:len(labels)-1]:
        # Zapisivanje elementa u zaseban red datoteke
        file.write(str(element) + '\n')

    file.write(str(labels[-1]))