# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:06:10 2021

@author: Maud
"""

from Functions_EEG_experiment import simulate_RW
import pandas as pd 
import sys, os
import numpy as np 

# Variables that can be adapted 
N_pp = 10 # Number of pp. used to generate the data 
N_reps_run = 10 # Number of repetitions executed within one run of this script
seed = 'seed23'

# One run of the file = one repetition: for each gruop 200 pp and their behaviour are simulated on the task 
groups = np.array([1, 2, 3])
participants = np.arange(0, N_pp, 1)

# Deduce the subset we're currently running
param = sys.argv[1:]   #Get the params from the command line (each repetition = different command)
assert len(param) == 1     #Checks whether there is only 1 parameter 
subset = int(param[0])

# Deduce which of the 1000 repetitions we're currently at
reps = np.arange(subset*N_reps_run, (subset+1)*N_reps_run, 1)

for rep_number in reps: 
    print("We're at repetition {}".format(rep_number))
    
    # import the true parameters generated all at once for this number of pp with random seed set to spec. value
    true_params_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', 
                                                     'True_parameters_{}pp_{}'.format(N_pp, seed))
    true_parameters_DF = pd.read_csv(os.path.join(true_params_folder, 'True_parameters_rep{}.csv'.format(rep_number)))
    print(true_parameters_DF.shape)
    
    for group in groups: 
        # for each group a response folder is created that will contain the LRs and the output files for this group 
        responses_foldername = 'Final_Simulations_group{}_{}pp_{}'.format(group, N_pp, seed)
        responses_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', responses_foldername)
        
        if not os.path.isdir(responses_folder): 
                os.makedirs(responses_folder)
        
        for pp in participants: 
            # relevant parameters for this participant 
            which_design = true_parameters_DF['Design_g{}'.format(group)][pp]
            LR = true_parameters_DF['LR_g{}'.format(group)][pp]
            Temp = true_parameters_DF['T_g{}'.format(group)][pp]
            print(which_design, LR, Temp)
            # select the design for this participant 
            design_filename = 'Data{}.csv'.format(which_design)
            Design_file = os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', design_filename)
            
            # generate the responses for this participant 
            total_reward, responses = simulate_RW(learning_rate = LR, design_file = Design_file, temperature = Temp, 
                                              triple_trials = True)
            if pp == 0: store_responses = responses
            else: store_responses = np.row_stack([store_responses, responses])
            
        responses_file = os.path.join(responses_folder, 'responses_group{}_rep{}.csv'.format(group, rep_number))
        np.savetxt(responses_file, store_responses, fmt = '%.i', delimiter = ',') 



