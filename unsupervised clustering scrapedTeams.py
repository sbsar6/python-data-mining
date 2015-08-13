import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from numpy.random import RandomState
import pylab

style.use("ggplot")


FEATURES = [ 'Rucks Won',  'Mauls Won', 'Metres Run'          ]
    

def Analysis():
    data= pd.DataFrame.from_csv("ScrapedCleanedTeams.csv")
     
    test_size =100
    X = np.array(data[FEATURES].values)#.tolist())
    X = preprocessing.scale(X)
    pca = PCA(n_components = 2, whiten = True)
    pca.fit(X)
    y = np.array(data["Team Name"].values.tolist())
    
    Y = pca.transform (X)
    X_pca=Y
    rng = RandomState(42)
    kmeans = KMeans(3,random_state=rng).fit(X_pca)
   
    
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
    plt.scatter(X_pca[:,0], X_pca[:,1],c=y )
    #plt.ylabel("Linebreak")
    #plt.xlabel("RucksNo")
    plt.legend()
    plt.show()
    

Analysis()   
    
