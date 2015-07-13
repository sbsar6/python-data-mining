import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']

def Build_Data_Set():
    data_df = pd.DataFrame.from_csv("key_stats_acc_perf_WITH_NA.csv")
    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.replace("NaN", 0).replace("N/A", 0)    
    #data_df = data_df[:100]
    X = np.array(data_df[FEATURES].values)#.tolist())

    y = (data_df["Status"]
         .replace("underperform",0)
         .replace("outperform", 1)
         .values.tolist())
    X = preprocessing.scale(X)
    return X,y


def Analysis():

    test_size =1000

    X, y = Build_Data_Set()
    print(len(X))
    
    clf = svm.SVC(kernel= "linear", C=1.0)

    clf.fit(X[:-test_size], y[:-test_size])

    correct_count = 0

    for x in range(1, test_size+1):
        if clf.predict(X[-x])[0] == y[-x]:
            correct_count +=1

    print("Accuracy: ", (correct_count/test_size) * 100.00)
    '''
    #helps visualise draw the line
    w= clf.coef_[0]

    a = -w[0] / w[1]

    xx = np.linspace(min(X[:,0]), max(X[:, 0]))

    yy = a * xx - clf.intercept_[0] / w[1]

    h0 = plt.plot(xx,yy, "k-", label="non weighted")
        # workd on arrays X[:,0] means 0th element of each layer (multi item element)
    plt.scatter(X[:,0], X[:,1], c = y)
    plt.ylabel("Trailing P?E")
    plt.xlabel("DE Ratio")
    plt.legend()
    plt.show()
    '''

def Randomizing():
    df = pd.DataFrame({"D1": range(5), "D2": range(5)})
    print(df)
    df2 = df.reindex(np.random.permutation(df.index))
    print(df2)
Analysis()   
    
#Randomizing()
