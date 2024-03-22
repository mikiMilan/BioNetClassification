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
X_train_c, y_train_c = remove_rand(X_train, y_train, 0.5)

model1 = SVC(class_weight='balanced', probability=True, random_state=42)
model2 = RandomForestClassifier(class_weight='balanced', random_state=42)
model21 = GradientBoostingClassifier(random_state=42)
model1.fit(X_train_c, y_train_c)
model2.fit(X_train_c, y_train_c)
model21.fit(X_train_c, y_train_c)

y_train_pred = model1.predict(X_train)
print(classification_report(y_train, y_train_pred))
y_train_pred = model2.predict(X_train)
print(classification_report(y_train, y_train_pred))
y_train_pred = model21.predict(X_train)
print(classification_report(y_train, y_train_pred))

threshold = 0.95

probabilities1 = model1.predict_proba(X_train)
candidates_for_removal1 = np.where(probabilities1[:, 0] > threshold)[0]
print("1. ", len(candidates_for_removal1))
probabilities2 = model2.predict_proba(X_train)
candidates_for_removal2 = np.where(probabilities2[:, 0] > threshold)[0]
print("2. ", len(candidates_for_removal2))
probabilities21 = model21.predict_proba(X_train)
candidates_for_removal21 = np.where(probabilities21[:, 0] > threshold)[0]
print("3. ", len(candidates_for_removal21))

candidates_for_removal = list(set(candidates_for_removal1) & set(candidates_for_removal2) & set(candidates_for_removal21))

print("4. ", len(candidates_for_removal))

X_train_b, y_train_b = np.delete(X_train, candidates_for_removal, axis=0), np.delete(y_train, candidates_for_removal)
model3 = SVC(class_weight='balanced')
model3.fit(X_train_b, y_train_b)
y_train_pred_b = model3.predict(X_train_b)
print(classification_report(y_train_b, y_train_pred_b))

print("-" * 50)

threshold = 0.95

#
X_test = np.array([embeddings[node] for node in unlabeled_nodes])
y_true = np.array([labels.get(node, 0) for node in unlabeled_nodes])

probabilities1 = model1.predict_proba(X_test)
candidates_for_removal1 = np.where(probabilities1[:, 0] > threshold)[0]
print("1. ", len(candidates_for_removal1))
probabilities2 = model2.predict_proba(X_test)
candidates_for_removal2 = np.where(probabilities2[:, 0] > threshold)[0]
print("2. ", len(candidates_for_removal2))
probabilities21 = model21.predict_proba(X_test)
candidates_for_removal21 = np.where(probabilities21[:, 0] > threshold)[0]
print("2. ", len(candidates_for_removal21))

candidates_for_removal = list(set(candidates_for_removal1) & set(candidates_for_removal2) & set(candidates_for_removal21))

print("3. ", len(candidates_for_removal))

X_test_b, y_true_b = np.delete(X_test, candidates_for_removal, axis=0), np.delete(y_true, candidates_for_removal)
y_true_pred_b = model3.predict(X_test_b)
print(classification_report(y_true_b, y_true_pred_b))
