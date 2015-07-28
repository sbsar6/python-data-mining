import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
from sklearn.decomposition import PCA
import pylab

style.use("ggplot")


FEATURES = ['RucksNo', 'PosGainline', 'NegGainline', 'Linebreak',
       'rdNear', 'rdRuck', 'rdFar', 'rdMiddle',
       'rsSlow', 'rsMedium', 'rsFast', 'KickTotal', 'KickedInfield',
       'KickedtoTouch', 'turnoverTot', 'turnoverKick', 'turnoverContact',
       'fromTurnover', 'penContact', 'Tries', 'TryTotal',
       'PenTotal']
    

def Analysis():
    data= pd.DataFrame.from_csv("all_games.csv")
    data_df = data[data["PhaseName"] == "BALL IN PLAY"] 
    test_size =100
    X = np.array(data_df[FEATURES].values)#.tolist())
    X = preprocessing.scale(X)
    pca = PCA(n_components = 2, whiten = True)
    pca.fit(X)
    y = np.array(data_df["penContact"].values.tolist())
    
    Y = pca.transform (X)
    #clf = svm.SVC(kernel= "linear", C=10.0)

    #clf.fit(X[:-test_size], y[:-test_size])

    #correct_count = 0

##    for x in range(1, test_size+1):
##        if clf.predict(X[-x])[0] == y[-x]:
##            correct_count +=1

    #print("Accuracy: ", (correct_count/test_size) * 100.00)
    
    #helps visualise draw the line
    '''w= clf.coef_[0]

    a = -w[0] / w[1]

    xx = np.linspace(min(X[:,0]), max(X[:, 0]))

    yy = a * xx - clf.intercept_[0] / w[1]

    h0 = plt.plot(xx,yy, "k-", label="non weighted")'''
        # workd on arrays X[:,0] means 0th element of each layer (multi item element)
    plt.scatter(Y[:,0], Y[:,1],c=y )
    #plt.ylabel("Linebreak")
    #plt.xlabel("RucksNo")
    plt.legend()
    plt.show()
    

Analysis()   
    
