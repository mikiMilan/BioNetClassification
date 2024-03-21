import random
import networkx as nx
import numpy as np


def load_graph(filename):
    graph = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            nodes = line.split("\t")  # ili "\t"
            graph.add_edge(nodes[0], nodes[1])

    return graph


def load_labels(filename):
    labels = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            labels[line] = 1

    return labels


def load_embeddings(filename, graph):
    embedding_dict = {}
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(" ")
            node = parts[0]
            if node in graph.nodes():
                embedding = np.array([float(x) for x in parts[1:]])
                embedding_dict[node] = embedding

    return embedding_dict


random.seed = 12754


def remove_rand(X, y, prob = 0.15):
    for i in range(len(y)-1, -1, -1):
        if (y[i] != 1) and (prob > random.random()):
            y = np.delete(y, i)
            X = np.delete(X, i, axis=0)

    return X, y


def remove_rand2(X, y, prob = 0.15):
    for i in range(len(y)-1, -1, -1):
        if prob > random.random():
            y = np.delete(y, i)
            X = np.delete(X, i, axis=0)

    return X, y

