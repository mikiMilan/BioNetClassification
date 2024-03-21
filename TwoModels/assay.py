import numpy as np
from unit import load_graph, load_labels, load_embeddings, remove_rand
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# loading
graph = load_graph("../data/yeast/BioGRID.txt")
labels = load_labels("../data/yeast/disprotYeast194.txt")
embeddings = load_embeddings("../data/vec/embed-origin-128.txt", graph)

labeled_nodes, unlabeled_nodes = train_test_split(list(graph.nodes()), test_size=0.3, random_state=42)

X_train = np.array([embeddings[node] for node in labeled_nodes])
y_train = np.array([labels.get(node, 0) for node in labeled_nodes])

# vjerovatnoca brisanja podatka labeliranog sa 0
prob = 0.9
# f1_socre za 1 prelazi 0.5 kada:
#   - prob=0.93, model2 = GaussianNB()
#   - prob=0.9, model2 = SVC(class_weight='balanced')
""""
!!! Treba probati i druge modele, jer male su 
sanse da prvi model pronađe toliko mnogo SIGURNIH nula
"""


# model2 = GaussianNB()
# model2 = RandomForestClassifier(class_weight='balanced')
model2 = SVC(class_weight='balanced') # znacajno losiji ako class_weight != 'balanced'
# model2 = GradientBoostingClassifier()
# model2 = KNeighborsClassifier(n_neighbors=3)
X_train_c, y_train_c = remove_rand(X_train, y_train, prob)
model2.fit(X_train_c, y_train_c)
# model2.fit(X_train, y_train)

y_train_pred_c = model2.predict(X_train_c)
print(classification_report(y_train_c, y_train_pred_c))
# y_train_pred = model2.predict(X_train)
# print(classification_report(y_train, y_train_pred))


print("-" * 50)

X_test = np.array([embeddings[node] for node in unlabeled_nodes])
y_true = np.array([labels.get(node, 0) for node in unlabeled_nodes])

X_test_c, y_true_c = remove_rand(X_test, y_true, prob)
y_pred_c = model2.predict(X_test_c)
print(classification_report(y_true_c, y_pred_c))
# y_pred = model2.predict(X_test)
# print(classification_report(y_true, y_pred))