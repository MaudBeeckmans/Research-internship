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


#%% Cell1: create the estimation_dataframe containing the estimates over all participants and all repetitions for all possible n_trials

    #when true: use all possible learning rates as 'simulations' instead of a certain group of 'participants' as simulations 
all_possible_LR = True

if all_possible_LR == False: group = 1 
else: group = 'allLR'
n_reps = 100 # number of repetitions for each 'simulation', for each repetition the LR will be estimated with all number of trials in trials


# Define the names of the folders containing the simulations and the one that will contain the estimations
    #Also define the learning_rates: their file_name depends on whether we're working with a certain 'group of participants' 
    #or all the learning rates 
if all_possible_LR == True: 
    N_simulations = 11
    simul_folder = 'Simulations_allLR_{}rep'.format(n_reps)
    estim_folder = 'Estimations_allLR_{}rep'.format(n_reps)
    learning_rates = pd.read_csv(os.path.join('Final_simul_est_files', 'allLR_overview.csv'))['LR']

else: 
    N_simulations = 80
    simul_folder = 'Simulations_group'
    estim_folder = 'Estimations_group{}_{}rep'.format(group, n_reps)
    learning_rates = pd.read_csv(os.path.join('Final_simul_est_files', 'pp_overview80_group{}.csv'.format(group)))['LR']

#Compute mean and std for the learning rates: will be used in the plots 
mean_LR = np.round(np.mean(learning_rates), 2)
std_LR = np.round(np.std(learning_rates), 3)

# name of the folder that will contain the estimations 
folder_name = os.path.join(os.getcwd(), 'Final_simul_est_files', estim_folder)
# array containing all the simulations that we want to use 
simulations = np.arange(0, N_simulations, 1)
# trials: array containing the different amounts of trials that will be used to do the parameter estimation 
trials = pd.read_csv(os.path.join(folder_name, 'Estimate_pp{}.csv'.format(0))).columns[2:-1]

# input_df: will contain the estimations for all repetitions and all possible amount of trials for this 'group'
input_df = pd.DataFrame(columns = np.concatenate([['simul', 'rep','real_param'], trials.astype(str)]))
for simul in simulations: 
    print("We're at simulation {}".format(simul))
    this_simul_DF = pd.read_csv(os.path.join(folder_name, 'Estimate_pp{}.csv'.format(simul)))
    n_reps = this_simul_DF.shape[0]
    for rep in range(n_reps): input_df = input_df.append({'simul':simul}, ignore_index = True)
    input_df.iloc[simul*n_reps:(simul+1)*n_reps, 1:] = this_simul_DF.iloc[:, :trials.shape[0]+2].to_numpy()
#save the dataframe, this is to ensure this cell should only be run once 
input_df.to_csv(os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary',
                             'Estimates_group{}_{}rep.csv'.format(group, n_reps)))
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
trials = input_df.columns[3:]
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
