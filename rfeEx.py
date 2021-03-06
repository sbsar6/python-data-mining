import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from predictive_analysis import feature_selection_RFE

fn = '7bips.csv'

fig,ax = plt.subplots(figsize=(10,10))
try:
    best = feature_selection_RFE(fn ,ax=ax, sel="all", goal="Linebreak", verbosity=0)
except:
    print('issue')

print ("The best features:", ', '.join(best))
plt.title("Feature Optimization for Gainline OPPoss")
plt.show()
