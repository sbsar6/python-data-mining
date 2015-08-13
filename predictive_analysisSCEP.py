#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Gameset analysis
"""
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


import matplotlib.pyplot as plt
from plot import plot_decision_line, plot_decision_boundary

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

def data_prepare(fn, sel=["Clean Breaks","Defenders Beaten"], goal="Outcome", verbosity=0):
    filename = os.path.join(datapath,fn)
    data_df = pd.DataFrame.from_csv(filename)
    if verbosity>0:
        print ("data_df:",data_df.shape,"columns:",list(data_df.columns))

    all_columns = ['Tries_Scored','Kick_at_Goal_Success', 'Drop_Goals',
       'Kicks_from_Hand', 'Passes', 'Runs', 'Metres_Run',
       'Possession(%)', 'Clean_Breaks', 'Defenders_Beaten', 'Offloads', 'Rucks_Won', 'Mauls_Won',
        'Turnovers_Conceded', 'Tackles_Made', 'Tackles_Missed',
       'Tackling_Success_Rate', 'Scrums_on_own_feed', 'Lineouts_on_own_feed', 'Penalties_Conceeded',
       'Yellow_Cards', 'Red_Cards']
    
    all_names = ['Tries_Scored','Kick_at_Goal_Success', 'Drop_Goals',
       'Kicks_from_Hand', 'Passes', 'Runs', 'Metres_Run',
       'Possession(%)', 'Clean_Breaks', 'Defenders_Beaten', 'Offloads', 'Rucks_Won', 'Mauls_Won',
        'Turnovers_Conceded', 'Tackles_Made', 'Tackles_Missed',
       'Tackling_Success_Rate', 'Scrums_on_own_feed', 'Lineouts_on_own_feed', 'Penalties_Conceeded',
       'Yellow_Cards', 'Red_Cards']
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

def game_analysis(fn,sclf,ax=None,sel=["Turnovers_Conceeded","Clean_Breaks"],toest=False,verbosity=0):
    X, y, names = data_prepare(fn, sel=sel, goal="Outcome", verbosity=verbosity-1)
  
    #class_weight = None
    class_weight = 'auto'
    
    sample_weight_constant = np.ones(len(X))
    
    weight_1 = np.sum(y<=0.5)/np.sum(y>0.5)
    sample_weight_1 = np.ones(len(X))
    sample_weight_1[y>0.5] = weight_1
    #print zip(y,sample_weight_1)

    if class_weight == 'auto':
        sample_weight = sample_weight_1
    else:
        sample_weight = sample_weight_constant 
   
    clf = get_clf(sclf,class_weight=class_weight)

    if toest==True:
        from kgml.modsel import cv_run
        n_cv=5
        res = cv_run(clf, X, y, random_state, n_cv=n_cv, scoring='accuracy')
        res = cv_run(clf, X, y, random_state, n_cv=n_cv, scoring='precision')
        res = cv_run(clf, X, y, random_state, n_cv=n_cv, scoring='recall')
        res = cv_run(clf, X, y, random_state, n_cv=n_cv, scoring='f1')
        #res = cv_run(clf, X, y, random_state, n_cv=n_cv, scoring='roc_auc')
    else: 
        if True:
            clf.fit(X, y)
        else:
            test_size = int(len(X)*0.5)
            clf.fit(X[:-test_size], y[:-test_size])
            correct_count = 0

            for x in range(1, test_size+1):
                if clf.predict(X[-x])[0] == y[-x]:
                    correct_count +=1

            if verbosity>0:
                print("Accuracy: ", (correct_count/test_size) * 100.00)
        title = "file:{}  model:{}  weights:{}".format(fn[:10],sclf,class_weight)
        if ax is None:
            fig,ax1 = plt.subplots(1)
        else:
            ax1 = ax
        plot_decision_boundary(clf, X, y, ax=ax1, sample_weight=sample_weight, names=names, title=title) 
        if ax is None:
            plt.show()

def predict_evaluate_models(fn ,ax=None, sel=["Turnovers_Conceeded","Clean_Breaks"], goal="Outcome", verbosity=0):
    class_weight = 'auto'
    X, y, names = data_prepare(fn, sel=sel, goal=goal, verbosity=verbosity-1)
    if verbosity > 2:
        y_shuffled = y.copy()
        np.random.shuffle(y_shuffled)
        print ("All zeros accuracy:",1.0-np.sum(y)/len(y)) 
        print ("y_shuffled f1_csore:",metrics.f1_score(y, y_shuffled))

    n_folds = 10
    cv = cross_validation.StratifiedKFold(y, n_folds=n_folds)
    #cv = cross_validation.LeaveOneOut(n=len(y))
    results = []
    for sclf in ('svm','svmp','svmr','lgCV','gnb','rf','knc'):
        clf = get_clf(sclf,class_weight=class_weight)
        y_pred = cross_validation.cross_val_predict(clf, X, y, cv=cv)
        #print "pred:",y_pred
        res = [
            metrics.accuracy_score(y, y_pred),
            metrics.precision_score(y, y_pred),
            metrics.recall_score(y, y_pred),
            metrics.f1_score(y, y_pred),
            ]
        if verbosity > 0:
            print (sclf,res) 
        results.append( (sclf,res) )

    return results

def feature_selection_ET(fn ,ax=None, sel="all", goal="Outcome", verbosity=0, nf=7):
    n_estimators=500
    X, y, names = data_prepare(fn, sel=sel, goal=goal, verbosity=verbosity-1)
    forest = ensemble.ExtraTreesClassifier(n_estimators=n_estimators,
                                  random_state=random_state,n_jobs=-1)
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
    nf_all = X.shape[1]
    for i in range(nf_all):
        print("%2d. %20s (%10f)" % (i+1, names[indices[i]], importances[indices[i]]))

    # Plot the feature importances of the forest
    nf = nf_all if nf > nf_all else nf
    ax.set_title("Feature importances")
    ax.bar(range(nf), importances[indices][:nf],
           color="r", yerr=std[indices][:nf], align="center")
    anames = np.array(names)
    ax.set_xlim([-1, nf])
    plt.xticks(range(nf), anames[indices][:nf],rotation='vertical')



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
    best = names[rfecv.ranking_==1]
    #print "The best features:", ', '.join(best)
    return best


def test(args):
    #predict_evaluate_models(args.fn,sel=args.sel,verbosity=2)
    if False:    
        fig,ax = plt.subplots()
        feature_selection_ET(args.fn ,ax=ax, sel="all", goal="Outcome", verbosity=2)
        plt.show()
    if True:
        fig,ax = plt.subplots()
        feature_selection_RFE(args.fn ,ax=ax, sel="all", goal="Outcome", verbosity=2)
        plt.show()
 
    print (sys.stderr,"Test OK")
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Commands.')
    parser.add_argument('cmd', nargs='?', default='test',help="make_train|make_test")
    parser.add_argument('-rs', type=int, default=None,help="random_state")
    parser.add_argument('-fn', type=str, default='ScapedCleaned.csv',help="filename to apply cmd")
    parser.add_argument('-clf', type=str, default='svm',help="classification model")
    parser.add_argument('-sel', type=str, default='two',help="features to select")
    
    args = parser.parse_args()
    print (sys.stderr,args) 
    if args.rs:
        random_state = int(args.rs)
    if random_state:
        random.seed(random_state)
        np.random.seed(random_state)

    if args.cmd == 'test':
        test(args)
    elif args.cmd == 'make':
        game_analysis(args.fn,args.clf,sel=args.sel,toest=True)
    else:
        raise ValueError("bad cmd")
    
