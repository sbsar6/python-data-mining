import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
from collections import Counter
from sklearn.metrics import accuracy_score
from sklearn.feature_selection import RFE
from sklearn import cross_validation
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from bokeh.palettes import brewer
palette = brewer["Blues"][3]
from bokeh.plotting import *
from bokeh.charts import Bar, show, output_file
import bokeh
from bokeh.plotting import figure, show
#from bokeh.palettes import Green3
import json

            
def machLearn(path):
    
    DataCSV = pd.read_csv(path)
    #DataCSV['Playing_Location'] = DataCSV['Playing_Location'].apply(lambda x: str(x).replace("home","1").replace("away","0"))
    #DataCSV['Penalties_Conceeded'] = DataCSV['Penalties_Conceeded'].apply(lambda x: float(str(x).split("(")[0])) 
    
    List = ["Scrum_Lost","Rucks_from_Hand","Opp_Lineout_Lost","Tackles_Missed", "Own_Scrum_Won","%Rucks_Won", "Tot_Own_Scrums","Defenders_Beaten", "Tackles_Made" ]
    columns = DataCSV.columns.values
    Features = [i for i in columns if str(i) in List]
    
    X = np.array(DataCSV[Features].values)
    X = preprocessing.scale(X,axis=0)
    
    y = np.array(DataCSV["Referee"].values)
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y)
    
    clf = svm.SVC(kernel="linear")
    clf.fit(X_train,y_train)
    rf = RandomForestClassifier(n_estimators = 150)
    rf.fit(X_train,y_train)
    
    
    scores_SVM = clf.score(X_test,y_test)
    scores_RF = rf.score(X_test,y_test)
    rfe = RFE(svm.SVC(kernel="linear"), n_features_to_select=1)
    rfe.fit(X,y)
        
    ranks = rfe.ranking_
    
    clf = ExtraTreesClassifier(n_estimators = 250,random_state=0)
    clf.fit(X,y)
    importance = clf.feature_importances_
    
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
    
    bar = Bar(ranks,features,title="Most Important Features for Determining Referee",palette=brewer["Purples"][3], stacked=True)
    
    output_file("rankings.html")
    show(bar)

    
    return ranks, importance, rankings, Features  
    

path = "EP7SeasonsCleaned.csv"
#path = "EP7SeasonsCleaned.csv"
a,b,c,d=machLearn(path)
