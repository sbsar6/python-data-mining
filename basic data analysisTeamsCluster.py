import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
style.use("ggplot")


FEATURES = [ 'Rucks Won', 'Mauls Won',
       'Kicks from Hand', 'Passes', 'Runs', 'Metres Run',
       'Possession(%)', 'Clean Breaks', 'Defenders Beaten', 'Offloads', 'Rucks Won',
        'Turnovers Conceded', 
       'Tackling Success Rate', 'Scrums on own feed', 'Lineouts on own feed', 'Penalties Conceeded'
            ]

    

def Analysis():
    data_df = pd.DataFrame.from_csv("ScrapedCleanedTeams.csv")
    test_size =100
    X = np.array(data_df[FEATURES].values)#.tolist())
    X = preprocessing.scale(X)
    
    y = np.array(data_df["Team Name"].values.tolist())
    
    print(len(X))
    print(len(y))
    
    clf = svm.SVC(kernel= "linear", C=10.0)

    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1, test_size+1):
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count +=1

    print("Accuracy: ", (correct_count/test_size) * 100.00)
    
    #helps visualise draw the line
    '''w= clf.coef_[0]

    a = -w[0] / w[1]

    xx = np.linspace(min(X[:,0]), max(X[:, 0]))

    yy = a * xx - clf.intercept_[0] / w[1]

    h0 = plt.plot(xx,yy, "k-", label="non weighted")'''
        # workd on arrays X[:,0] means 0th element of each layer (multi item element)
    plt.scatter(X[:,0], X[:,1], c = y)
    plt.ylabel("Linebreak")
    plt.xlabel("RucksNo")
    plt.legend()
    plt.show()
    

Analysis()   
    
