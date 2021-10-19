# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 16:10:16 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat


#%% Cell 1: create the learning_rates file 
group = 'allLR' #group should be the group number of 'allLR' when using all possible learning rates instead of a certain 'group of pp'

n_reps = 100 # number of repetitions for each 'simulation', for each repetition the LR will be estimated with all number of trials in trials


# Define the names of the folders containing the simulations and the one that will contain the estimations
    #Also define the learning_rates: their file_name depends on whether we're working with a certain 'group of participants' 
    #or all the learning rates 
if group == 'allLR': 
    N_simulations = 11
    simul_folder = 'Simulations_allLR_{}rep'.format(n_reps)
    estim_folder = 'Estimations_allLR_{}rep'.format(n_reps)
    learning_rates = pd.read_csv(os.path.join('Final_simul_est_files', 'allLR_overview.csv'))['LR']

else: 
    N_simulations = 80
    simul_folder = 'Simulations_group'
    estim_folder = 'Estimations_group{}_{}rep'.format(group, n_reps)
    learning_rates = pd.read_csv(os.path.join('Final_simul_est_files', 'pp_overview80_group{}.csv'.format(group)))['LR']

learning_rates.to_csv(os.path.join('Final_simul_est_files', 'learning_rates_group{}.csv'.format(group)))

#%% Cell 2: create the estimation_dataframe containing the estimates over all participants and all repetitions for all possible n_trials

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