import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np

class classifier:
    def __init__(self,X,y):
        self.X = X
        self.y = y
    def analysis_svm(self):
        clf = svm.SVC(kernel="linear")
        clf.fit(self.X,self.y)
        return clf
    def predict(self,X_test,y_test):
        clf = self.analysis_svm()
        predictions = clf.predict(X_test)
        for i, prediction in enumerate(predictions):
            print ('Prediction: %s. Original: %s' % (prediction, y_test[i])) 

Features = ['RucksNo', 'PosGainline', 'NegGainline', 'Linebreak',
       'rdNear', 'rdRuck', 'rdFar', 'rdMiddle',
       'rsSlow', 'rsMedium', 'rsFast', 'KickTotal', 'KickedInfield',
       'KickedtoTouch', 'turnoverTot', 'turnoverKick', 'turnoverContact',
       'fromTurnover', 'penContact', 'Tries', 'TryTotal',
       'PenTotal']            

def read_csv(path):
    return pd.read_csv(path)

def wrangle(path):
    
    Data = read_csv(path)
    
    List = [1.0,0.0]
    dictionary = {}

    for obj in List:
        dictionary[obj] = Data[Data["penFK"] == obj]
    Zeroes = dictionary[List[0]]
    
    FeaturesDictionary = {}

    for name in List:
        DataFea = dictionary[name]

        Un = DataFea["Unnamed: 0"].tolist()
        features_list = []
        for j in range(len(Un)):
            Data = []
            for i in range(len(Features)):
                value = DataFea[DataFea["Unnamed: 0"]==Un[j]][Features[i]].tolist()[0]
                Data.append(value)
            features_list.append(Data)
        FeaturesDictionary[name] = features_list
    
    test = []
    training = []

    for key in FeaturesDictionary.keys():
        print(key)
        test.append(FeaturesDictionary[key][-3:])
        training.append(FeaturesDictionary[key][:-3])

    ones_list = [1] * 209
    zeroes_list = [0] * 2162
    ones_test_list = [1] * 3
    zeroes_test_list = [0] * 3

    Labels = np.array(ones_list +zeroes_list)
    FeaturesList = np.array(training[1] + training[0])

    model = classifier(FeaturesList,Labels)
    
    LabelsTest = np.array(ones_test_list + zeroes_test_list)
    FeaturesTestList = np.array(test[1] + test[0])

    model.predict(FeaturesTestList,LabelsTest)
