
from __future__ import division
import csv, random, sys, datetime, os
import numpy as np
import pandas as pd
import warnings

#from config import datapath
datapath = "C:\\Users\\Andrew\\Desktop\\python data mining"
random_state = 1

from sklearn import preprocessing, decomposition
from sklearn import svm, linear_model, ensemble, naive_bayes, neighbors
from sklearn import cross_validation, grid_search, metrics
from sklearn.feature_selection import RFECV
from collections import Counter

import matplotlib.pyplot as plt
from plot import plot_decision_line, plot_decision_boundary

fig,ax = plt.subplots(figsize=(10,10))
data_df = pd.DataFrame.from_csv("EPAllSeasonsCleaned.csv")
#if verbosity>0:
#    print ("data_df:",data_df.shape,"columns:",list(data_df.columns))
List = ["Unnamed:_0","Team_Name","Outcome","Result"]
columns = data_df.columns.values
Features = [i for i in columns if str(i) not in List]
print(Features)

Labels = [1.0,0.0]
    
#Populating a dictionary accordingly with each label
dictionary = {}
for Label in Labels:
    dictionary[Label] = data_df[data_df["Outcome"] == Label]
#print (dictionary)
bucket = data_df["Outcome"].tolist()
freqs = Counter(bucket)
print(freqs)


FeaturesDictionary = {}
for Label in Labels:
    DataFeatures = dictionary[Label]

#Creating a list with unique values, it works as an identifier for each row 
'''UniqueValuesList = DataFeatures.index.tolist()
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
'''
#To remove drawn games
ones_list = [1] * freqs[1] 
zeroes_list = [0] * freqs[0]    
y = np.array(data_df['Outcome'].values)



X = np.array(data_df[Features].values)
X = preprocessing.scale(X,axis=0)

clf = svm.SVC(kernel= "linear", C= 1.0, class_weight=None)
estimator = clf    
scoring = 'f1'
cv = cross_validation.StratifiedKFold(y, 2)

if True:
    rfecv = RFECV(estimator=estimator, step=1, cv=cv, scoring=scoring)
else:
    from kgml.rfecv import RFECVp
    f_estimator = clf
    rfecv = RFECVp(estimator=estimator,f_estimator=f_estimator, step=1, cv=cv, scoring=scoring)
    
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    rfecv.fit(X, y)



ax.set_xlabel("Number of features selected")
ax.set_ylabel("Cross validation score ({})".format(scoring))
ax.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)

print("Optimal number of features : %d" % rfecv.n_features_)
best = names[rfecv.ranking_==1]
print ("The best features:", ', '.join(best))

