print(__doc__)
import csv, random, sys, datetime, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn import svm, preprocessing
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
from sklearn import cross_validation, grid_search, metrics
from sklearn.feature_selection import RFECV
from sklearn.datasets import make_classification
datapath = "C:\\Users\\Andrew\\Desktop\\python data mining"
#datapath = path +'\\GameData'
fn = "ScapedCleaned.csv"
fig,ax = plt.subplots(figsize=(10,10))


def data_prepare(fn, sel=["Clean Breaks","Defenders Beaten"], goal="Outcome", verbosity=0):
    filename = os.path.join(datapath,fn)
    data_df = pd.DataFrame.from_csv(filename)
    if verbosity>0:
        print ("data_df:",data_df.shape,"columns:",list(data_df.columns))

    all_columns = ['Conversions', 'Kick at Goal Success', 'Drop Goals',
       'Kicks from Hand', 'Passes', 'Runs', 'Metres Run',
       'Possession(%)', 'Clean Breaks', 'Defenders Beaten', 'Offloads', 'Rucks Won',
        'Turnovers Conceded', 'Tackles Made', 'Tackles Missed',
       'Tackling Success Rate', 'Scrums on own feed', 'Lineouts on own feed', 'Penalties Conceeded',
       'Yellow Cards', 'Red Cards']

    all_names = ['Conversions', 'Kick at Goal Success', 'Drop Goals',
       'Kicks from Hand', 'Passes', 'Runs', 'Metres Run',
       'Possession(%)', 'Clean Breaks', 'Defenders Beaten', 'Offloads', 'Rucks Won',
        'Turnovers Conceded', 'Tackles Made', 'Tackles Missed',
       'Tackling Success Rate', 'Scrums on own feed', 'Lineouts on own feed', 'Penalties Conceeded',
       'Yellow Cards', 'Red Cards']
    two_names = ["Clean Breaks","Defenders Beaten"]

    if isinstance(sel,(list,tuple)) or sel=='two':
        if sel == 'two': sel = two_names
        X = np.array(data_df[sel].values)
        X = preprocessing.scale(X,axis=0)
        names = sel
    else: 
        X = np.array(data_df[all_names].values)
        X = preprocessing.scale(X,axis=0)
        if sel[:6]=='decomp':
            decomp = sel[6:]
            names = ["Comp1","Comp2"]
            if decomp == 'PCA':
                X = decomposition.PCA(2).fit_transform(X)
            else:
                from sklearn.cluster import FeatureAgglomeration
                X = FeatureAgglomeration(n_clusters=2).fit_transform(X)
        elif sel == 'all':
            names = all_names
        else:
            raise ValueError("bad sel: {}".format(sel))

    y = np.array(data_df[goal].values)
    if verbosity>0:
        print ("X:",X.shape, "y:",y.shape)

    return X,y,np.array(names)


def feature_selection_RFE(fn ,ax=None, sel="all", goal="Outcome", verbosity=0, nf=7):
    X, y, names = data_prepare(fn, sel=sel, goal=goal, verbosity=verbosity-1)
    if verbosity > 1:
        print ("names:", ",".join(names))
    
    # Create the RFE object and compute a cross-validated score.
    #estimator = svm.SVC(kernel="linear",C=1.0)
    estimator = get_clf('svm')    
    scoring = 'f1'
    cv = cross_validation.StratifiedKFold(y, 2)

    # The "accuracy" scoring is proportional to the number of correct
    # classifications
    if True:
        rfecv = RFECV(estimator=estimator, step=1, cv=cv, scoring=scoring)
    else:
        from kgml.rfecv import RFECVp
        f_estimator = get_clf('svm')
        rfecv = RFECVp(estimator=estimator,f_estimator=f_estimator, step=1, cv=cv, scoring=scoring)
        
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rfecv.fit(X, y)

    # Plot number of features VS. cross-validation scores
    ax.set_xlabel("Number of features selected")
    ax.set_ylabel("Cross validation score ({})".format(scoring))
    ax.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)

    #print("Optimal number of features : %d" % rfecv.n_features_)
    best = names[rfecv.ranking_==1], rfecv.grid_scores
    #print "The best features:", ', '.join(best)
    return best
def get_clf(sclf,C=1.0,class_weight=None):
    if sclf == 'svm':
        clf = svm.SVC(kernel= "linear", C=C, class_weight=class_weight)
    elif sclf == 'svmr':
        clf = svm.SVC(kernel= "rbf", gamma=0.5, C=1, class_weight=class_weight)
    elif sclf == 'svmp':
        clf = svm.SVC(kernel= "poly", degree=3, gamma=0.1, C=5, class_weight=class_weight)
    elif sclf == 'lg1':
        clf = linear_model.LogisticRegression(penalty='l1', C=C, class_weight=class_weight)
    elif sclf == 'lg2':
        clf = linear_model.LogisticRegression(penalty='l2', C=C, class_weight=class_weight)
    elif sclf == 'lgCV':
        clf = linear_model.LogisticRegressionCV(penalty='l2', class_weight=class_weight)
    elif sclf == 'ridgeCV':
        clf = linear_model.RidgeCV()
    elif sclf == 'rf':
        from sklearn.ensemble import RandomForestClassifier
        if not hasattr(RandomForestClassifier,'coef_'):
            RandomForestClassifier.coef_ = property(lambda self:self.feature_importances_)
        clf = RandomForestClassifier(n_estimators=100, max_depth=2, min_samples_leaf=2,
            class_weight=class_weight)
    elif sclf == 'gnb':
        clf = naive_bayes.GaussianNB()
    elif sclf == 'knc':
        clf = neighbors.KNeighborsClassifier(n_neighbors=5)
    else:
        raise ValueError("bad sclf: {}".format(sclf))
    return clf
best = feature_selection_RFE(fn ,ax=ax, sel="all", goal="Outcome", verbosity=0)
plt.show()
print ("The best features:", ', '.join(best))
