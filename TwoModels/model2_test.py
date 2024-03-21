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

model1 = SVC(class_weight='balanced', probability=True)
X_train_c, y_train_c = remove_rand(X_train, y_train, 0.95)
model1.fit(X_train_c, y_train_c)
# model1.fit(X_train, y_train)

# y_train_pred_c = model1.predict(X_train_c)
# print(classification_report(y_train_c, y_train_pred_c))
#
y_train_pred = model1.predict(X_train)
print(classification_report(y_train, y_train_pred))

probabilities = model1.predict_proba(X_train)
threshold = 0.5
candidates_for_removal = np.where(probabilities[:, 0] > threshold)[0]
# print(len(candidates_for_removal))
# for i in candidates_for_removal:
#     if y_train[i] == 1:
#         print("--", i, y_train_pred[i])
len(candidates_for_removal)

X_train_b, y_train_b = np.delete(X_train, candidates_for_removal, axis=0), np.delete(y_train, candidates_for_removal)
model2 = SVC(class_weight='balanced')
model2.fit(X_train_b, y_train_b)
y_train_pred_b = model2.predict(X_train_b)
print(classification_report(y_train_b, y_train_pred_b))

print("-" * 50)
#
X_test = np.array([embeddings[node] for node in unlabeled_nodes])
y_true = np.array([labels.get(node, 0) for node in unlabeled_nodes])

y_pred = model1.predict(X_test)
print(classification_report(y_true, y_pred))

probabilities = model1.predict_proba(X_test)
threshold = 0.8
candidates_for_removal = np.where(probabilities[:, 0] > threshold)[0]

X_test_c, y_true_c = np.delete(X_test, candidates_for_removal, axis=0), np.delete(y_true, candidates_for_removal)
y_pred_c = model2.predict(X_test_c)
print(classification_report(y_true_c, y_pred_c))
