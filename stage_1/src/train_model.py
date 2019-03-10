from utility import *
from sklearn import svm, tree, linear_model, ensemble
from sklearn.metrics import recall_score, precision_score, make_scorer, classification_report
from sklearn.model_selection import cross_validate, StratifiedKFold

WORDPATH =  "../data/etc/words.txt"
DATASETDIR = "../data/"
TRAINFILEPATH = "../data/train.txt"
TESTFILEPATH = "../data/test.txt"

def get_dataset(train = True):
	features = []
	labels = []
	dataset_path = TRAINFILEPATH if train else TESTFILEPATH
	with open(dataset_path, 'r') as fi:
		lines = fi.readlines()
		for line in lines:
			fi_features, fi_labels = sample_data(DATASETDIR+line.strip(), worddir)
			#print(len(fi_features), len(fi_labels))
			features += fi_features
			labels += fi_labels
			#print(len(features))
	return features, labels

def cross_validation(model, features, labels):
    precision_scorer = make_scorer(precision_score, pos_label=1)
    recall_scorer = make_scorer(recall_score, pos_label=1)
    scoring = {'precision': precision_scorer,
               'recall': recall_scorer}
    skf = StratifiedKFold(n_splits=5)
    scores = cross_validate(model, features, labels, scoring=scoring,
                cv=skf, return_train_score=False)
    print('Cross validation result:')
    precision = scores['test_precision'].mean()
    recall = scores['test_recall'].mean()
    print('precision = %f, recall = %f' % (precision, recall))
    print('f1 = %f' % ((2 * precision * recall) / (precision + recall)))

def test_score(model, test_features, test_labels):
	predicts = model.predict(test_features)
	print('Test result:')
	print(classification_report(test_labels, predicts, labels=[1]))

if __name__ == "__main__":
	worddir = load_worddir(WORDPATH)
	#print(len(worddir), worddir['alien'])
	features, labels = get_dataset()
	print(len(features))
	cnt = 0
	for label in labels:
		cnt += (label == 1)
	print(cnt)
	# features = features[0:1000]
	# labels = labels[0:1000]

	test_features, test_labels = get_dataset(train=False)
	print(len(test_features))

	models = [
    	# linear_model.RidgeClassifierCV(normalize=True),
    	# linear_model.LogisticRegressionCV(n_jobs=-1),
    	# tree.DecisionTreeClassifier(criterion='entropy'),
    	ensemble.RandomForestClassifier(n_jobs=-1),
    	# svm.SVC(kernel='rbf')
	]

	for model in models:
		print("start", model)
		cross_validation(model, features, labels)
		model.fit(features, labels)
		test_score(model, test_features, test_labels)
		print("end", model)