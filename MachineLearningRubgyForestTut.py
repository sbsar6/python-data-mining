import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE
from sklearn import cross_validation
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from plot import plot_decision_line, plot_decision_boundary

#class to create a classifier (model)
class classifier:
    def __init__(self,X,y):
        self.X = X
        self.y = y
        self.X_train, self.X_test, self.y_train, self.y_test = cross_validation.train_test_split(self.X,self.y)
    def cross(self):
        return self.X_train, self.X_test, self.y_train, self.y_test
    def analysis_svm(self,X_Train,Y_Train):
        clf = svm.SVC(kernel="linear")
        clf.fit(X_Train,Y_Train)
        return clf
    def Forest(self,X_Train,Y_Train):
        clf = ExtraTreesClassifier(n_estimators = 250,random_state=0)
        clf.fit(X_Train,Y_Train)
        return clf.feature_importances_
    def RandomForest(self,X_Train,Y_Train):
        rf = RandomForestClassifier(n_estimators = 150)
        rf.fit(X_Train,Y_Train)
        return rf
    def recursive(self):
        rfe = RFE(svm.SVC(kernel="linear"), n_features_to_select=1)
        rfe.fit(self.X,self.y)
        return rfe.ranking_
    def analysis_linear_regression(self,X_Train,Y_Train):
        clf = LinearRegression()
        clf.fit(X_Train,Y_Train)
        return clf
    def acurracy(self,clf):
        return clf.score(self.X_test,self.y_test)
    def predict(self,X_test,y_test,clf):
        predictions = clf.predict(X_test,y_test)
        for i, prediction in enumerate(predictions):
            print('Prediction: %s. Original: %s' % (prediction, y_test[i])) 
            
            
def wrangle3(path):
    
    DataCSV = pd.read_csv(path)
    #DataCSV['Playing_Location'] = DataCSV['Playing_Location'].apply(lambda x: str(x).replace("home","1").replace("away","0"))
    #DataCSV['Penalties_Conceeded'] = DataCSV['Penalties_Conceeded'].apply(lambda x: float(str(x).split("(")[0])) 
    
    List = ["Unnamed:_0","Team_Name","Outcome","Result"]
    columns = DataCSV.columns.values
    Features = [i for i in columns if str(i) not in List]
    print (Features)
    Labels = [1.0,0.0]
    
    #Populating a dictionary accordingly with each label
    dictionary = {}
    for Label in Labels:
        dictionary[Label] = DataCSV[DataCSV["Outcome"] == Label]
    #print (dictionary)
    bucket = DataCSV["Outcome"].tolist()
    freqs = Counter(bucket)
    print(freqs)
    
    #Features dictionary
    FeaturesDictionary = {}
    for Label in Labels:
        DataFeatures = dictionary[Label]
        
        #Creating a list with unique values, it works as an identifier for each row 
        UniqueValuesList = DataFeatures.index.tolist()
        features_list = []
        for j in range(len(UniqueValuesList)):
            Data = []
            for each_feature in range(len(Features)):
                value = DataFeatures[DataFeatures.index==UniqueValuesList[j]][Features[each_feature]].tolist()[0]
                Data.append(value)
            features_list.append(Data)
        FeaturesDictionary[Label] = features_list
    #print(features_list)
    #print (FeaturesDictionary)    
    ValuesFeatures = [FeaturesDictionary[key] for key in FeaturesDictionary.keys()]
    X = ValuesFeatures[1] + ValuesFeatures[0]
    
    ones_list = [1] * freqs[1] 
    zeroes_list = [0] * freqs[0]
    
    y = np.array(ones_list + zeroes_list)
    
    classifier_object = classifier(X,y)
    
    Xtrain, Xtest, ytrain, ytext = classifier_object.cross()
    
    clf = classifier_object.analysis_svm(Xtrain,ytrain)
    rf = classifier_object.RandomForest(Xtrain,ytrain)
    
    scores_SVM = classifier_object.acurracy(clf)
    scores_RF = classifier_object.acurracy(rf)
    
    ranks = classifier_object.recursive()
    
    importance = classifier_object.Forest(Xtrain,ytrain)
    
    sorted_index = np.argsort(importance)[::-1]
    
    ax.set_xlabel("Number of features selected")
    ax.set_ylabel("Cross validation score ({})".format(scoring))
    ax.plot(range(1, len(ranks.grid_scores_) + 1), ranks.grid_scores_)

    print("Optimal number of features : %d" % ranks.n_features_)
    best = names[ranks.ranking_==1]
    print ("The best features:", ', '.join(best))

    '''
    forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)

    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(10):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(10), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(10), indices)
    plt.xlim([-1, 10])
    plt.show()
    '''


    print("acurracy SVM:",scores_SVM)
    print("acurracy Random Forest:",scores_RF)

    place = 1
    print("results using TreesClassifier")
    for i,j in zip(np.array(Features)[sorted_index],importance[sorted_index]):
        print("rank: {0}, {1}, {2}".format(place,i,j))
        place += 1
    
    print("----------------------------")
    print("----------------------------")
    place = 1
    print("results using RFE")
    print (sorted(zip(map(lambda x: round(x, 4), ranks), Features)))   
    return ranks, importance     



path = "EPAllSeasonsCleaned.csv"
a,b = wrangle3(path)
