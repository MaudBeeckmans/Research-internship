# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 16:22:57 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat

N_pp = 80
folder_name = os.path.join(os.getcwd(), 'Estimations')
participants = np.arange(0, N_pp, 1)
# trials = np.array([100, 200, 300, 400, 480])
trials =  np.array([200, 480, 480*2, 480*3])

input_df = pd.DataFrame(columns = np.concatenate([['pp', 'rep','real_param'], trials.astype(str)]))
for pp in participants: 
    pp_DF = pd.read_csv(os.path.join(folder_name, 'Estimate_pp{}.csv'.format(pp)))
    n_reps = pp_DF.shape[0]
    for rep in range(n_reps): input_df = input_df.append({'pp':pp}, ignore_index = True)
    input_df.iloc[pp*n_reps:(pp+1)*n_reps, 1:] = pp_DF.iloc[:, :trials.shape[0]+2].to_numpy()
#%%
learning_rates = pd.read_csv('pp_overview80.csv')['LR']
for rep in range(n_reps): 
    used_df = input_df[input_df["rep"].isin([rep])]
    correlations = np.empty(shape = (n_reps, trials.shape[0]))
    col_count = 0 #keep track of which column of the correlation array has to be filled in 
    for trial in trials: 

        alpha_est = used_df[trial.astype(str)].to_numpy().astype(float)
        alpha_est = np.round(alpha_est, 3)
        
        #Power option A
        cor = np.round(np.corrcoef(learning_rates, alpha_est)[0, 1], 2)
        correlations[rep, col_count] = cor
        col_count += 1
power_cut_off = 0.8
power = np.mean((correlations > power_cut_off)*1, axis = 0) #take the average across each column
   #result will be one power-value per n_trials-value (now only over 20 repetitions so not really reliable though)

fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.set_ylim([0, 1.1])
axes.set_xlim([0, 500])
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0)
axes.plot(trials, power, 'ro')
axes.set_title("{} pp, power = P(corr(p_est, p) > {})".format(N_pp, power_cut_off))

    





    # fig, axes = plt.subplots(nrows = 1, ncols = 1)
    # axes.plot(learning_rates, alpha_est, 'o')
    # axes.set_title('Correlation with {} trials and {} pp: {}'.format(trial, N_pp, cor))
    # axes.set_xlabel('real LR', loc = 'right')
    # axes.set_ylabel('esimated LR', loc = 'center')
    
    # #Power option B
    # realLR_G1 = alpha_real[:int(N_pp/2)]
    # realLR_G2 = alpha_real[int(N_pp/2):]
    # estLR_G1 = alpha_est[:int(N_pp/2)]
    # estLR_G2 = alpha_est[int(N_pp/2):]
    # T_stat_real, P_value_real = stat.ttest_ind(realLR_G1, realLR_G2) 
    # T_stat_est, P_value_est = stat.ttest_ind(estLR_G1, estLR_G2) 
    # print('P-value for real LR: {}, P-value for estimate LR: {}'.format(P_value_real, P_value_est))
