################################
### Script python para teste ###
################################

import base_2 as base
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os
import random
import seaborn as sns
import warnings

  
print(len(base.get_price_total()[0:-4]))

print(len(base.no_filter().resample('W').sum()))
