from utility import *
from sklearn import svm, tree, linear_model, ensemble
from sklearn.metrics import recall_score, precision_score, make_scorer
from sklearn.model_selection import cross_validate, StratifiedKFold

WORDPATH =  "../data/etc/words.txt"
DATASETDIR = "../data/"
TRAINFILEPATH = "../data/train.txt"

def get_dataset(train = True):
	features = []
	labels = []
	dataset_path = DATASETDIR+TRAINFILEPATH if train else ""
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

if __name__ == "__main__":
	worddir = load_worddir(WORDPATH)
	#print(len(worddir), worddir['alien'])
	features, labels = get_dataset()

	models = [
    	linear_model.RidgeClassifierCV(normalize=True),
    	# linear_model.LogisticRegressionCV(),
    	tree.DecisionTreeClassifier(criterion='entropy'),
    	ensemble.RandomForestClassifier(),
    	svm.SVC(kernel='rbf')
	]

	for model in models:
		print("start", model)
		model.fit(features, labels)
		cross_validation(model, features, labels)
		print("end", model)