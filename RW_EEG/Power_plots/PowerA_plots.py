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


#%% Cell1: preparations; load the correct learning rates (learning_rates) and estimations dataframe (input_df)

group = 2 #when using allLR, put group to 'allLR'
n_reps = 100
used_simulations = 80

learning_rates = pd.read_csv(os.path.join(os.getcwd(), 'Final_simul_est_files', 
                                          'learning_rates_group{}.csv'.format(group)))['LR'][:used_simulations*n_reps]

input_df_path = os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary')
input_df = pd.read_csv(os.path.join(input_df_path, 
                                       'Estimates_group{}_{}rep.csv'.format(group, n_reps))).iloc[:used_simulations*n_reps, :]
trials = input_df.columns[4:] 
#Compute mean and std for the learning rates: will be used in the plots 
mean_LR = np.round(np.mean(learning_rates), 2)
std_LR = np.round(np.std(learning_rates), 3)


#%% Cell2: compute the correlations for each repetition and each possible number of trials and estimate the power

"""If want to combine groups: 
    # group = 1
    # learning_rates_g1 = pd.read_csv(os.path.join('Final_simul_est_files', 'pp_overview80_group{}.csv'.format(group)))['LR']
    # group= 2
    # learning_rates_g2 = pd.read_csv(os.path.join('Final_simul_est_files', 'pp_overview80_group{}.csv'.format(group)))['LR']
    # learning_rates = np.concatenate([learning_rates_g1, learning_rates_g2])
    # mean_LR = np.round(np.mean(learning_rates), 2)
    # std_LR = np.round(np.std(learning_rates), 3)
    # input_DF_g1 = pd.read_csv(os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary', 'Estimates_group1_100rep.csv'))
    # input_DF_g2 = pd.read_csv(os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary', 'Estimates_group2_100rep.csv'))
    # input_df = pd.concat([input_DF_g1, input_DF_g2])
    """


correlations = np.empty(shape = (n_reps, trials.shape[0]))
n_reps = int(np.max(input_df['rep'])+1)
N_simulations = int(np.max(input_df['simul'])+1)


for rep in range(n_reps): 
    used_df = input_df[input_df["rep"].isin([rep])]
    col_count = 0 #keep track of which column of the correlation array has to be filled in 
    for trial in trials: 

        alpha_est = used_df[trial].to_numpy().astype(float)
        alpha_est = np.round(alpha_est, 3)
        
        #Power option A
        cor = np.round(np.corrcoef(learning_rates, alpha_est)[0, 1], 2)
        correlations[rep, col_count] = cor
        col_count += 1
power_cut_off = 0.8
power = np.mean((correlations > power_cut_off)*1, axis = 0) #take the average across each column
   #result will be one power-value per n_trials-value (now only over 20 repetitions so not really reliable though)


#%% Cell 3: Plot the power (x-axis = the number of trials used to estimate the LR; y-axis = the power)
fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.set_ylim([-0.1, 1.1])
axes.set_xlim([0, int(trials[-1])])
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0)
axes.plot(trials.astype(int), power, 'ro')
axes.set_title("{} pp with mean LR {}, std {}, \npower = P(corr(p_est, p) > {}) with {} reps".format(N_simulations, 
                                                                mean_LR, std_LR, power_cut_off, n_reps))

    

#%% Cell 4: Plot cor(LR_real, LR_est) for one of the repetitions (chosen randomly)
choose_rep = np.random.randint(n_reps)
n_cols = 4
fig, axes = plt.subplots(nrows = 2, ncols = n_cols, sharex = True, sharey = True)
fig.suptitle('Correlations with {} simulations, group {}'.format(N_simulations, group))
count = 0
for n_trials in trials: 
    alpha_est = used_df[n_trials].to_numpy().astype(float)
    cor = np.round(np.corrcoef(learning_rates, alpha_est)[0, 1], 2)
    axes[int(count/n_cols), count%n_cols].plot(learning_rates, alpha_est, 'o')
    axes[int(count/n_cols), count%n_cols].set_title('{} trials: cor = {}'.format(n_trials, cor))
    axes[int(count/n_cols), count%n_cols].set_xlabel('real LR', loc = 'center')
    axes[int(count/n_cols), count%n_cols].set_ylabel('esimated LR', loc = 'center')
    axes[int(count/n_cols), count%n_cols].set_xlim(0, 1.1)
    axes[int(count/n_cols), count%n_cols].set_ylim(0, 1.1)
    count += 1
