import networkx as nx
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, f1_score

# loading graph
G = nx.Graph()
with open("data/yeast/BioGRID_withoutLeaves.txt", 'r') as file:
    for line in file:
        line = line.strip()
        nodes = line.split(" ") # ili "\t"
        G.add_edge(nodes[0], nodes[1])
print(G)

# loading embedding
embedding_dict = {}
with open("data/vec/embed-wol-64.txt", "r") as file:
    for line in file:
        parts = line.strip().split(" ")
        node = parts[0]
        embedding = np.array([float(x) for x in parts[1:]])
        embedding_dict[node] = embedding

# labeling
labels = {}
with open("data/yeast/disprotYeast194_withoutLeaves.txt", 'r') as file:
    for line in file:
        line = line.strip()
        labels[line] = 1

# adjacency_matrix = nx.adjacency_matrix(G)
# adjacency_matrix_dense = adjacency_matrix.toarray()

# separation
labeled_nodes, unlabeled_nodes = train_test_split(list(G.nodes()), test_size=0.2, random_state=42)
print('Broj oznacenih cvorova:', len(labeled_nodes))
print('Broj neoznacenih cvorova:', len(unlabeled_nodes))

# create train set
X_train = np.array([embedding_dict[node] for node in labeled_nodes])
y_train = np.array([labels.get(node, 0) for node in labeled_nodes])

# training
# model = LogisticRegression()
# model = SVC()
# model = DecisionTreeClassifier() #-> dao neke jedinice, ali na losim pozicijama
# model = RandomForestClassifier()
# model = GradientBoostingClassifier()
# model = KNeighborsClassifier()
model = GaussianNB() # najbolji ali loše
model.fit(X_train, y_train)

# prediction
X_test = np.array([embedding_dict[node] for node in unlabeled_nodes])
y_pred = model.predict(X_test)

# evaluation
y_true = np.array([labels.get(node, 0) for node in unlabeled_nodes])
# print(y_true)
# print(y_pred)

accuracy = accuracy_score(y_true, y_pred)
r1_test_1 = f1_score(y_true,y_pred, pos_label=1)
r1_test_0 = f1_score(y_true,y_pred, pos_label=0)
print("Model accuracy on 20% labeled nodes:", accuracy)
print("F1, test, 1:", r1_test_1)
print("F1, test, 0:", r1_test_0)

