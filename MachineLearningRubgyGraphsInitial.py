import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE
from sklearn import cross_validation
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier

from bokeh.plotting import *
from bokeh.charts import Bar, show, output_file
import bokeh
from bokeh.plotting import figure, show

import json

#bokeh.plotting.output_notebook()

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
    #Import data and perpare for machine learning
    DataCSV = pd.read_csv(path)
       
    List = ["Unnamed:_0","Team_Name","Outcome","Result",""]
    columns = DataCSV.columns.values
    Features = [i for i in columns if str(i) not in List]
    
    Labels = [1.0,0.0]
    
    #Populating a dictionary accordingly with each label
    dictionary = {}
    for Label in Labels:
        dictionary[Label] = DataCSV[DataCSV["Outcome"] == Label]
    
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
        
    ValuesFeatures = [FeaturesDictionary[key] for key in FeaturesDictionary.keys()]
    X = ValuesFeatures[1] + ValuesFeatures[0]
    
    ones_list = [1] * freqs[1] 
    zeroes_list = [0] * freqs[0]
    from sklearn import preprocessing
    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    # standardize the data attributes
    standardized_X = preprocessing.scale(X)
    
    y = np.array(ones_list + zeroes_list)
    
    #classifier_object = classifier(X,y)
    from sklearn import metrics
    from sklearn.ensemble import ExtraTreesClassifier
    model = ExtraTreesClassifier()
    model.fit(X, y)
    # display the relative importance of each attribute
    print(model.feature_importances_)
    
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    # create the RFE model and select 3 attributes
    rfe = RFE(model, 3)
    rfe = rfe.fit(X, y)
    #    summarize the selection of the attributes
    print(rfe.support_)
    print(rfe.ranking_)

    from sklearn import metrics
    from sklearn.tree import DecisionTreeClassifier
    # fit a CART model to the data
    model = DecisionTreeClassifier()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


    from sklearn import metrics
    from sklearn.svm import SVC
    # fit a SVM model to the data
    model = SVC()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    '''Xtrain, Xtest, ytrain, ytext = classifier_object.cross()
    
    clf = classifier_object.analysis_svm(Xtrain,ytrain)
    rf = classifier_object.RandomForest(Xtrain,ytrain)
    
    scores_SVM = classifier_object.acurracy(clf)
    scores_RF = classifier_object.acurracy(rf)
    
    ranks = classifier_object.recursive()
    
    importance = classifier_object.Forest(Xtrain,ytrain)
    
    sorted_index = np.argsort(importance)[::-1]
    
    print("acurracy SVM:",scores_SVM)
    print("acurracy Random Forest:",scores_RF)

    place = 1
    
    rankings = {}
    
    print("results using TreesClassifier")
    for i,j in zip(np.array(Features)[sorted_index],importance[sorted_index]):
        rankings[place] = [i,j]
        print("rank: {0}, {1}, {2}".format(place,i,j))
        place += 1
    
    print("----------------------------")
    print("----------------------------")
    place = 1
    print("results using RFE")
    print(sorted(zip(map(lambda x: round(x, 4), ranks), Features)))   
    
    ranks = [value[1] for value in rankings.values()]
    features = [value[0] for value in rankings.values()]

    bar = Bar(ranks,features,title="EP and SR Feature Rankings",stacked=True)
    output_file("rankings.html")
    show(bar)

    
    return ranks, importance, rankings, Features  
    '''


path = "EP7SeasonsCleaned.csv"
wrangle3(path)

