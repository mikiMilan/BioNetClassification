import networkx as nx
from node2vec import Node2Vec


def ntv(G, embedding_file):
    node2vec = Node2Vec(G, dimensions=32, walk_length=20, num_walks=4, workers=3)
    # node2vec = Node2Vec(G, dimensions=32, walk_length=80, num_walks=25, workers=2)
    # node2vec = Node2Vec(G, dimensions=16, walk_length=40, num_walks=10, workers=2)
    model = node2vec.fit()

    with open(embedding_file, "w") as file:
        for node in model.wv.index_to_key:
            embedding = model.wv[node]
            line = node + " " + " ".join(map(str, embedding)) + "\n"
            file.write(line)


file_path = "data/yeast/BioGRID_withoutLeaves.txt"
G = nx.Graph()

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        nodes = line.split(" ") # ili "\t"
        # print(nodes)
        G.add_edge(nodes[0], nodes[1])
print(G)

ntv(G, 'data/vec/embed-wol-32.txt')