print(__doc__)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification

# Build a classification task using 3 informative features
'''X, y = make_classification(n_samples=1000, n_features=25, n_informative=3,
                           n_redundant=2, n_repeated=0, n_classes=8,
                           n_clusters_per_class=1, random_state=0)
'''
FEATURES = ['RucksNo', 'PosGainline', 'NegGainline', 'Linebreak',
       'rdNear', 'rdRuck', 'rdFar', 'rdMiddle',
       'rsSlow', 'rsMedium', 'rsFast', 'KickTotal', 'KickedInfield',
       'KickedtoTouch', 'turnoverTot', 'turnoverKick', 'turnoverContact',
       'fromTurnover', 'penContact', 'Tries', 'TryTotal',
       'PenTotal']
data= pd.DataFrame.from_csv("all_games.csv")
data_df = data[data["PhaseName"] == "BALL IN PLAY"] 
   
X = np.array(data_df[FEATURES].values)#.tolist())
X = preprocessing.scale(X)
y = np.array(data_df["PosGainline"].values.tolist())

# Create the RFE object and compute a cross-validated score.
svc = SVC(kernel="linear")
# The "accuracy" scoring is proportional to the number of correct
# classifications
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(y, 2),
              scoring='accuracy')
rfecv.fit(X, y)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()
