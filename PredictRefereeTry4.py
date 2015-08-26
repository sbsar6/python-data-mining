import pandas as pd
from sklearn import linear_model, svm, preprocessing
import numpy as np
from collections import Counter
from bokeh.palettes import brewer
palette = brewer["Blues"][3]

def machLearn(path):
    
    DataCSV = pd.read_csv(path)
    #DataCSV['Playing_Location'] = DataCSV['Playing_Location'].apply(lambda x: str(x).replace("home","1").replace("away","0"))
    #DataCSV['Penalties_Conceeded'] = DataCSV['Penalties_Conceeded'].apply(lambda x: float(str(x).split("(")[0])) 
    
    Referees = DataCSV["Referee"].tolist()
    RefereesCount = Counter(Referees)

    RefereesSelection = [referee for referee in set(Referees) if RefereesCount[referee] > 140]
    
    Frames = []
    for Referee in RefereesSelection:
        frame = DataCSV[DataCSV["Referee"] == Referee]
        Frames.append(frame)
    result = pd.concat(Frames)
    
    
    List = ["Unnamed:_0","Team_Name","Referee","Result"]
    columns = result.columns.values
    Features = [i for i in columns if str(i) not in List]
    
    X = np.array(result[Features].values)
    X = preprocessing.scale(X,axis=0)
    
    y = np.array(result["Referee"].values)
    
    
    classifier_object = classifier(X,y)
    
    Xtrain, Xtest, ytrain, ytext = classifier_object.cross()
    
    clf = classifier_object.analysis_svm(Xtrain,ytrain)
    rf = classifier_object.RandomForest(Xtrain,ytrain)
    
    scores_SVM = classifier_object.acurracy(clf)
    scores_RF = classifier_object.acurracy(rf)
    
    ranks = classifier_object.recursive(Xtrain,ytrain)
    
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
    
    bar = Bar(ranks,features,title="Dragons Feature Rankings BIP Tries",palette=brewer["Purples"][3], stacked=True)
    
    output_file("rankings.html")
    show(bar)

    
    return ranks, importance, rankings, Features  

path = "EP7SeasonsCleaned.csv"
#path = "EP7SeasonsCleaned.csv"
machLearn(path)
