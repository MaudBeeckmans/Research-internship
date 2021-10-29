# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:06:10 2021

@author: Maud
"""

from Functions_EEG_experiment import simulate_RW, generate_parameters
import pandas as pd 
import sys, os
import numpy as np 

# Variables that can be adapted 
N_pp = 200 # Number of pp. used to generate the data 
N_reps_run = 20 # Number of repetitions executed within one run of this script
seed = 'seedset'

# One run of the file = one repetition: for each gruop 200 pp and their behaviour are simulated on the task 
groups = np.array([1, 2, 3])
LR_means = np.array([0.6, 0.7, 0.8]) # True mean LR for each group
LR_std = 0.1 # True std LR for all groups (constant over groups)
Temp_mean = 0.4 # True mean Temp for all groups (constant over groups)
Temp_std = 0.2 # # True std Temp for all groups (constant over groups)
temp_type = 'variable' # temperature is not fixed, there is some variation over the participants 


# Deduce the subset we're currently running
param = sys.argv[1:]   #Get the params from the command line (each repetition = different command)
assert len(param) == 1     #Checks whether there is only 1 parameter 
subset = int(param[0])

# a different random seed is set each time the script is ran 
np.random.seed(subset)

# Deduce which of the 1000 repetitions we're currently at
reps = np.arange(subset*N_reps_run, (subset+1)*N_reps_run, 1)

for rep_number in reps: 
    print("We're at repetition {}".format(rep_number))

    participants = np.arange(0, N_pp, 1)
    true_parameters_DF = pd.DataFrame(columns = ['LR_g1', 'LR_g2', 'LR_g3', 
                                                 'T_g1', 'T_g2', 'T_g3', 
                                                 'Design_g1', 'Design_g2', 'Design_g3', 'Seed'],index = participants)
    true_parameters_DF['Seed'] = subset
    
    # An LR & temp folder is created that will contain the LRs and temperatures stored for all groups in 1 file 
    param_foldername = 'True_parameters_{}pp_{}'.format(N_pp, seed)
    param_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', param_foldername)
    if not os.path.isdir(param_folder): 
        os.makedirs(param_folder)
    
    for group in groups: 
        # for each group a response folder is created that will contain the LRs and the output files for this group 
        responses_foldername = 'Final_Simulations_group{}_{}pp_{}'.format(group, N_pp, seed)
        responses_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', responses_foldername)
        
        if not os.path.isdir(responses_folder): 
                os.makedirs(responses_folder)
        
        # for each group compute the true LRs; true Temperatures and the design_file used for each participant
        true_parameters_DF['LR_g{}'.format(group)]= generate_parameters(mean = LR_means[group-1], std = LR_std, n_pp = N_pp)
        true_parameters_DF['T_g{}'.format(group)] = generate_parameters(mean = Temp_mean, std = Temp_std, n_pp = N_pp)
        true_parameters_DF['Design_g{}'.format(group)]= np.random.randint(0, 10, size = N_pp)
        
        
        for pp in participants: 
            # relevant parameters for this participant 
            which_design = true_parameters_DF['Design_g{}'.format(group)][pp]
            LR = true_parameters_DF['LR_g{}'.format(group)][pp]
            Temp = true_parameters_DF['T_g{}'.format(group)][pp]
            
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
    
    true_parameters_DF.to_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep_number)))



