# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 15:59:24 2021

@author: Maud
"""
import pandas as pd 
import os
import numpy as np 

#%% Function to generate parameters from normal distribution with certain mean and std 
def generate_parameters(mean = 0.1, std = 0.05, n_pp = 1):
    """Function to generate the learning rate or the temperatures for multiple participants: 
        - parameters are randomly chosen from normal distribution with mean = mean & std = std
        - one unique parameter is generated for each participant"""
    parameters = np.round(np.random.normal(loc = mean, scale = std, size = n_pp), 3)
    while np.any(parameters >= 1) or np.any(parameters <= 0): 
        parameters = np.where(parameters >= 1, 
                            np.round(np.random.normal(loc = mean, scale = std, size = 1), 3), 
                            parameters)
        parameters = np.where(parameters <= 0, 
                              np.round(np.random.normal(loc = mean, scale = std, size = 1), 3), 
                              parameters)
    return parameters

#%%

seed_number = None
nreps = 10
N_pp = 10
# np.random.seed(seed_number)

groups = np.array([1, 2, 3])
LR_means = np.array([0.6, 0.7, 0.8]) # True mean LR for each group
LR_std = 0.1 # True std LR for all groups (constant over groups)
Temp_mean = 0.4 # True mean Temp for all groups (constant over groups)
Temp_std = 0.2 # # True std Temp for all groups (constant over groups)
seed = 'seed{}'.format(seed_number)

participants = np.arange(0, N_pp, 1)

for rep in range(nreps): 
    true_parameters_DF = pd.DataFrame(columns = ['LR_g1', 'LR_g2', 'LR_g3', 
                                                 'T_g1', 'T_g2', 'T_g3', 
                                                 'Design_g1', 'Design_g2', 'Design_g3'],index = participants)
    
    # An LR & temp folder is created that will contain the LRs and temperatures stored for all groups in 1 file 
    param_foldername = 'True_parameters_{}pp_{}'.format(N_pp, seed)
    param_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', param_foldername)
    if not os.path.isdir(param_folder): 
        os.makedirs(param_folder)
    
    for group in groups: 
        # for each group compute the true LRs; true Temperatures and the design_file used for each participant
        true_parameters_DF['LR_g{}'.format(group)]= generate_parameters(mean = LR_means[group-1], std = LR_std, n_pp = N_pp)
        true_parameters_DF['T_g{}'.format(group)] = generate_parameters(mean = Temp_mean, std = Temp_std, n_pp = N_pp)
        true_parameters_DF['Design_g{}'.format(group)]= np.random.randint(0, 10, size = N_pp)
    
    true_parameters_DF.to_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep)))
    
    
    