# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 15:39:30 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 

letters = ['A', 'B', 'C', 'D', 'Z']
n_pp = 20

from matplotlib import pyplot as plt 

power_A = 'Power_corr' + str(0.9)
power_B = 'Power_signif_diff'
power_options = [power_A, power_B]
power_file = os.path.join(os.getcwd(), 'Power_estimates')
fig, axes = plt.subplots(nrows = 2, ncols = 1)
for i in range(2): 
    axes[i].set_ylim([0, 1.1])
    axes[i].set_xlim([0, 50])
    axes[i].set_xlabel('N_trials', loc = 'right')
    y_label = axes[i].set_ylabel('P', loc = 'top')
    y_label.set_rotation(0)
for letter in letters: 
    power_dataframe = pd.read_csv(power_file + '\Power_df_20pp' + letter + '.csv')
    for i in range(2): 
        axes[i].plot(power_dataframe['n_trials'], power_dataframe[power_options[i]], 'o', label = 'dataset' + letter)
    axes[0].set_title("{} pp, power = P(corr(p_est, p) > {})".format(n_pp, 0.9))
    axes[1].set_title("{} pp, power = P(pgroup1 < pgroup2) p-value <= {}".format(n_pp, 0.05))
axes[0].legend()