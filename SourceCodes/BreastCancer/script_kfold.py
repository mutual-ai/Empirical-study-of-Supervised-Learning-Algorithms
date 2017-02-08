from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import numpy as np
from numpy import genfromtxt, savetxt
import sys
import random
from sklearn.cross_validation import KFold

def print_misclassification_error(a):
	dataset = genfromtxt(open('data.csv','r'), delimiter=',', dtype='f8')[0:]

	#Remove the rows with values 'NaN'
	dataset = dataset[~np.isnan(dataset).any(axis=1)]

	#Shuffling the dataset
	np.random.shuffle(dataset)

	size = len(dataset)

	size_train = np.ceil(a/100.0*size)
	
	training = dataset[:size_train]
	test = dataset[size_train:]

	training_labels = [x[10] for x in training]
	training_data = [x[1:10] for x in training]

	test_labels = [x[10] for x in test]
	test_data = [x[1:10] for x in test]

	training_data=np.asarray(training_data)
	training_labels=np.asarray(training_labels)
	test_data=np.asarray(test_data)
	test_labels=np.asarray(test_labels)
	
	kf = KFold(int(size_train), n_folds=30)
	rf = RandomForestClassifier(n_estimators=100)
	#print training_data.size()
	clf = svm.SVC(C=0.01,kernel="linear")
	
	for train_index, test_index in kf:
		X_train, X_test = training_data[train_index], test_data[test_index]
		y_train, y_test = training_labels[train_index], test_labels[test_index]
		rf.fit(X_train,y_train)
		clf.fit(X_train,y_train)
		
	predict_rf = rf.predict(test_data)

	actual = np.array(test_labels)
	predicted_rf = np.array(predict_rf)

	error_rf = np.sum(actual!=predicted_rf)

	#SVM
	
	#clf.fit(training_data,training_labels)
	predict_svm = clf.predict(test_data)
	predicted_svm = np.array(predict_svm)
	
	#print predicted_svm
	error_svm = np.sum(actual!=predicted_svm)
	
	misclassification_error_rf = error_rf/(len(test_data)*1.0)*100
	misclassification_error_svm = error_svm/(len(test_data)*1.0)*100
	print "Misclassification Error using Random Forest : %f" % misclassification_error_rf
	print "Misclassification Error using SVM : %f" % misclassification_error_svm
	
	
	



if __name__ == '__main__':
    print_misclassification_error(float(sys.argv[1]))














