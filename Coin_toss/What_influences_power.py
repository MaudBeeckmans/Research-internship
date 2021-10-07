# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 14:54:52 2021

@author: Maud
"""

"""Script for investigating the 50 datasets drawn from populations with mean_g1 = 0.4, mean_g2 = 0.7
and std = 0.2. Each dataset has 20 participants."""

import pandas as pd
import numpy as np 
import os 
import pandas as pd 
from matplotlib import pyplot as plt 


power_file = os.path.join(os.getcwd(), 'Power_estimates2')

letters = np.arange(1, 50, 1).astype(str)
for letter in letters: 
    power_dataframe = pd.read_csv(power_file + '\Power_df_20pp' + letter + '.csv')
    power_dataframe['DF']= np.repeat(letter, power_dataframe.shape[0]).astype(list)
    if letter == '1': 
        big_power_df = power_dataframe
    else: 
        big_power_df= pd.concat([big_power_df, power_dataframe])
    


#%%

"""Correlate mean difference and power at n_trials = T"""

numbers = np.arange(1, 50, 1).astype(str)
all_ES = np.array([])
all_diff = np.array([])
all_pooled_std = np.array([])
for number in numbers: 
    power_DF = big_power_df[big_power_df['DF'] == number]
    ES = np.round(power_DF['ES'][0], 2)
    all_ES = np.append(all_ES, ES)
    diff = np.round(power_DF['group_diff'][0], 2)
    all_diff = np.append(all_diff, diff)
    pooled_std = np.round(np.sqrt(power_DF['STD_G1'][0]**2 + power_DF['STD_G2'][0]**2), 2)
    all_pooled_std = np.append(all_pooled_std, pooled_std)
    print('\nDataframe {}: \nES = {}, diff = {}, std = {}'.format(number, ES, diff, pooled_std))

def plot_correlation(corr_with = all_ES,which_ntrial = 10, fig_ax = 'ES'):
    
    trial_selection = which_ntrial
    trial_df = big_power_df[big_power_df['n_trials'] == trial_selection]
    PowerB_T = trial_df['Power_signif_diff']
    PowerA_T = trial_df['Power_corr0.9']
    select_ES = corr_with[trial_df['DF'].values.astype(int) -1 ]
    
    corA = np.round(np.corrcoef(PowerA_T, select_ES)[0, 1], 2)
    corB = np.round(np.corrcoef(PowerB_T, select_ES)[0, 1], 2)
    print('cor(powerA, {}) = {}, cor(powerB, {}) = {} at trial {}'.format(fig_ax, corA, fig_ax,
                                                                          corB, trial_selection))
    
    combine_25 = np.column_stack([np.round(PowerA_T.values, 2), np.round(PowerB_T.values, 2), select_ES])
    
    fig, axes = plt.subplots(nrows = 2, ncols = 1)
    axes[0].plot(combine_25[:, 0], combine_25[:,2], 'ro')
    axes[0].set_xlabel('PowerA_T{}'.format(trial_selection))
    axes[1].plot(combine_25[:, 1], combine_25[:,2], 'yo')
    axes[1].set_xlabel('PowerB_T{}'.format(trial_selection))
    axes[0].set_ylabel(fig_ax)
    axes[1].set_ylabel(fig_ax)
    axes[0].set_title('Correlation: {}'.format(corA))
    axes[1].set_title('Correlation: {}'.format(corB))
    fig.tight_layout()
    folder = os.path.join(os.getcwd(), 'Plots', 'Influences_plots')
    fig.savefig(folder + str('\Corr_Pow_{}_T{}.png'.format(fig_ax, which_ntrial)))

n_trials = np.arange(5, 55, 5)
for n_trial in n_trials: 
    plot_correlation(all_pooled_std, n_trial, fig_ax = 'pooled_std')
    plot_correlation(all_ES, n_trial, fig_ax = 'ES')
    plot_correlation(all_diff, n_trial, fig_ax = 'mean_diff')






