import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE
from sklearn import cross_validation

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
        #print("Accuracy: ",accuracy_score(y_test, predictions))

#features to create the model, just as the real estate example that I used to illustrate supervised learning,
#these features are our property size, age, etc              
Features = ['RucksNo', 'PosGainline', 'NegGainline', 'Linebreak',
       'rdNear', 'rdRuck', 'rdFar', 'rdMiddle',
       'rsSlow', 'rsMedium', 'rsFast', 'KickTotal', 'KickedInfield',
       'KickedtoTouch', 'turnoverTot', 'turnoverKick', 'turnoverContact',
       'fromTurnover', 'penContact', 'Tries', 'TryTotal',
       'PenTotal']            

def wrangle(path):
    
    DataCSV = pd.read_csv(path)
    
    #Labels (1 and 0)
    Labels = [1.0,0.0]
    
    #Populating a dictionary accordingly with each label
    dictionary = {}
    for Label in Labels:
        dictionary[Label] = DataCSV[DataCSV["penFK"] == Label]
        
    bucket = DataCSV["penFK"].tolist()
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
    
    y = np.array(ones_list + zeroes_list)
    
    classifier_object = classifier(X,y)
    
    Xtrain, Xtest, ytrain, ytext = classifier_object.cross()
    
    clf = classifier_object.analysis_svm(Xtrain,ytrain)
    
    scores = classifier_object.acurracy(clf)
    ranks = classifier_object.recursive()
    
    print("acurracy using cross-validation:",scores)
    for i in range(len(ranks)):
        print("rank:{0}, {1}".format(ranks[i],Features[i]))
    
    return scores, ranks

wrangle('all_gamesBIP.csv')   
