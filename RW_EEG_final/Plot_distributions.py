# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 12:47:58 2021

@author: Maud
"""
import matplotlib.pyplot as plt
import numpy as np
import os 
import pandas as pd
import seaborn as sns


#%% Cell to run for files from RW_EEG_final
temp_type = 'variable' # should be 'variable' or 'fixedat{}'
n_reps = 100
reps = np.arange(0, n_reps, 1)
#reps = np.delete(reps, np.array([0, 9, 13]))
groups = np.array([1, 2, 3])

n_pp = 200
seed = '_seed23'
if seed == '_seed24': groups = np.array([0])


power_folder = os.path.join(os.getcwd(), 'Power', 'Power_Temp{}_{}pp{}_{}reps'.format(temp_type, n_pp, seed, n_reps))
plot_folder = os.path.join(power_folder, 'Distribution_plots')
if not os.path.isdir(plot_folder): os.makedirs(plot_folder)

for group in groups: 
    print("we're at group {}".format(group))
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    axes.set_xlim(-0.5, 1.5)
    base_folder = os.path.join(os.getcwd(), 'LREstimations', 'LREstimations_group{}_Temp{}_{}pp{}'.format(group, 
                                                                                                    temp_type, n_pp, seed))
    for rep in reps: 
        LR_estimation_df = pd.read_csv(os.path.join(base_folder, 'LREstimate_rep{}.csv'.format(rep))).iloc[:, 1:]
        if rep == 0: 
            columns = LR_estimation_df.columns
            LR_estimates = LR_estimation_df
        else: LR_estimates = pd.concat([LR_estimates, LR_estimation_df])
    columns = np.array(['Real_LR', '1400', '1440'])
    for col in columns: 
        LR_estimates_col = np.array(LR_estimates[col])
        sns.kdeplot(LR_estimates_col, label = col, ax = axes)
        axes.legend()
    fig.suptitle('Group {}'.format(group))
    fig.savefig(os.path.join(plot_folder, 'Distributions_group{}'.format(group)))


#%% Cell to run for files from RW_EEG

groups = np.array([1, 2, 3]) #group should be the group number of 'allLR' when using all possible learning rates instead of a certain 'group of pp'
temp_type = 'variable'
n_reps = 100 # number of repetitions for each 'simulation', for each repetition the LR will be estimated with all number of trials in trials
reps = np.arange(0, n_reps, 1)
N_simulations = 80 # number of simulations 
used_temperature = 0.41
if temp_type == 'variable': used_temperature = None
plot_folder = os.path.join(r'C:\Users\Maud\Documents\Psychologie\2e master psychologie\Research Internship\Start to model RI\Projects\RW_EEG\Final_power_plots', 
                           'Temperature_{}@{}'.format(temp_type, used_temperature), 'Plot_distributions')
if not os.path.isdir(plot_folder): os.makedirs(plot_folder)

for group in groups: 
    if group == 3 and used_temperature == 0.41: 
        n_reps = 1000
        reps = np.arange(0, n_reps, 1)
    LR_filename = 'Estimates_group{}_{}rep_temp{}@{}.csv'.format(group, n_reps, temp_type, used_temperature)
    LR_file = os.path.join(r'C:\Users\Maud\Documents\Psychologie\2e master psychologie\Research Internship\Start to model RI\Projects\RW_EEG',
                           'Final_simul_est_files', 'Estimations_summary',LR_filename)
    print("we're at group {}".format(group))
    LR_estimation_df = pd.read_csv(LR_file).iloc[:, 3:]
    True_LR_folder = r'C:/Users/Maud/Documents/Psychologie/2e master psychologie/Research Internship/Start to model RI/Projects/RW_EEG/Final_simul_est_files'
    True_LR_file = os.path.join(True_LR_folder, 'learning_rates_group{}_Temp{}.csv'.format(group, temp_type))
    True_LRs = pd.read_csv(True_LR_file).iloc[:, 1]
    LR_estimation_df.iloc[:, 0] = True_LRs
    # Create the figure
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    axes.set_xlim(-0.5, 1.5)
    LR_estimates = LR_estimation_df
    columns = np.array(['real_param', '100', '960', '1440'])
    for col in columns: 
        LR_estimates_col = np.array(LR_estimates[col])
        sns.kdeplot(LR_estimates_col, label = col, ax = axes)
        axes.legend()
    fig.suptitle('Group {}'.format(group))
    fig.savefig(os.path.join(plot_folder, 'Distributions_group{}'.format(group)))
    
    