import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score

#class to create a classifier (model)
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
            print('Prediction: %s. Original: %s' % (prediction, y_test[i])) 
        print("Accuracy: ",accuracy_score(y_test, predictions))

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

        #Creating a list with unique values, to work as an identifier for each row 
        UniqueValuesList = DataFeatures.index.tolist()
        features_list = []
        for j in range(len(UniqueValuesList)):
            Data = []
            for Feature in Features:
                value = DataFeatures[DataFeatures.index==UniqueValuesList[j]][Feature].tolist()[0]
                Data.append(value)
            features_list.append(Data)
        FeaturesDictionary[Label] = features_list
    
    #splitting original lists into test and training, the training values will create the model(classifier), 
    #the test values will verify the quality of our model
    test = []
    training = []

    for key in FeaturesDictionary.keys():
        print(key)
        test.append(FeaturesDictionary[key][-20:])
        #the training values will have the last ten values for each label
        training.append(FeaturesDictionary[key][:-20])
    
    #labels vector for the training data
    ones_training_list = [1] * (freqs[1] - 20) #label 1 -> 202 times (the original data had 212 times)
    zeroes_training_list = [0] * (freqs[0] - 20) #label 0 -> 2155 times (the original data had 2165)
    
    Labels = np.array(ones_training_list + zeroes_training_list)
    FeaturesList = np.array(training[1] + training[0])
    
    #labels vector for the test data
    ones_test_list = [1] * 20
    zeroes_test_list = [0] * 20

    model = classifier(FeaturesList,Labels)
    
    LabelsTest = np.array(ones_test_list + zeroes_test_list)
    FeaturesTestList = np.array(test[1] + test[0])

    model.predict(FeaturesTestList,LabelsTest)

wrangle("all_gamesOPPhase.csv")
