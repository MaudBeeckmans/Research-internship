# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 10:51:54 2021

@author: Maud
"""

from Functions_EEG_experiment import likelihood
import os, sys
import numpy as np 
from scipy import optimize
import pandas as pd 


N_pp = 200 # number of pp used 

groups= np.array([1, 2, 3]) # for which groups you'd like to do the parameter estimation 
# the different n_trials that will be used to generate the parameter estimates
trials = np.concatenate([np.array([50]), np.arange(100, 1500, 100), np.array([1440])])
# temperature is estimated 
temp_type = 'variable' 
participants = np.arange(0, N_pp, 1)


# Define for which simulation we'll currently do the estimations at each repetition with each possible number of trials in trials used for the estimation
rep_number = sys.argv[1:] #Get the params 
# print(simul_number)
assert len(rep_number) == 1     #Checks whether there are n params
rep_number = int(rep_number[0])

# Deduce the parameters for this repetition 
param_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', 'True_parameters_{}pp'.format(N_pp))
param_DF = pd.read_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep_number)))

# define the folders where the LR estimates and the Temperature estimates will be stored (each repetition)
base_LRfolder = os.path.join(os.environ.get('VSC_SCRATCH'), 'RW_EEG_final', 'Estimations_LR')
base_Tempfolder = os.path.join(os.environ.get('VSC_SCRATCH'), 'RW_EEG_final', 'Estimations_Temp')

# if the folders don't exist yet, create the folders 
folders = [base_LRfolder, base_Tempfolder]

for group in groups:
    print('Estimations for group {} started'.format(group))
    design_array = param_DF['Design_g{}'.format(group)]
    # get the responses from this participant (are stored in a csv-file)
    response_foldername = 'Final_Simulations_group{}_Tempvariable_{}pp'.format(group, N_pp)
    response_file = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', response_foldername, 
                                 'responses_group{}_rep{}.csv'.format(group, rep_number))
    responses_allpp = pd.read_csv(response_file, header = None)
    
    #where will the LR and Temperature estimations be stored
    LREstimation_folder = os.path.join(base_LRfolder, 'LREstimations_group{}_Temp{}_{}pp'.format(group, 
                                                                                        temp_type, N_pp))
    TempEstimation_folder = os.path.join(base_Tempfolder, 'TempEstimations_group{}_Temp{}_{}pp'.format(group, 
                                                                                        temp_type, N_pp))
    folders = [LREstimation_folder, TempEstimation_folder]
    for folder in folders: 
        if not os.path.isdir(folder): os.makedirs(folder)
    
    # Create the file (with path) to which the estimation_DFs will be written eventually 
    LREstimation_file = os.path.join(LREstimation_folder, 'LREstimate_rep{}.csv'.format(rep_number))
    TempEstimation_file = os.path.join(TempEstimation_folder, 'TempEstimate_rep{}.csv'.format(rep_number))
    
    # Create the dataframe that will contain all the estimations for this simulation (shape will be: n_reps x n_cols)
    LREstimation_DF = pd.DataFrame(columns = np.concatenate([['Real_LR'], trials.astype(str)]), 
                                   index = np.arange(0, N_pp))
    TempEstimation_DF = pd.DataFrame(columns = np.concatenate([['Real_Temp'], trials.astype(str)]), 
                                     index = np.arange(0, N_pp))
    
    # fill in the true parameters
    LREstimation_DF['Real_LR'] = param_DF['LR_g{}'.format(group)]
    TempEstimation_DF['Real_Temp'] = param_DF['T_g{}'.format(group)]
    
    
    for pp in participants: 
        if pp%50 == 0: print("\n\nWe're at pp {}\n\n".format(pp))
        # the start design: containing the stimuli and FB at each trial for this pp.
        start_design = pd.read_csv(os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', 
                                                   'Data{}.csv'.format(design_array[pp])))
        # start design is repeated 3x to generate 1440 trials instead of 480 trials
        start_design = start_design.append(start_design).append(start_design)
        start_design['Response'] = responses_allpp.iloc[pp, :]
        
        for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
            # estimate the parameters given the start_design; n_trials defines how many trials are used to estimate the parameter(s) 
            estim_param = optimize.fmin(likelihood, np.random.rand(2), args =(tuple([start_design, n_trials])), 
                                maxfun= 1000, xtol = 0.001)
            LR_estim = estim_param[0]

            estimation_repeat = 0
            while LR_estim < 0.01 and estimation_repeat < 5:
                print('\nRepetition of estimation was !! for pp {} from rep {} with {} n_trials.'.format(pp, 
                                                                        rep_number, n_trials))
                estim_param = optimize.fmin(likelihood, np.random.rand(2), args =(tuple([start_design, n_trials])), 
                                maxfun= 1000, xtol = 0.001)
                LR_estim = estim_param[0]
                estimation_repeat += 1
            if LR_estim < 0.01 or LR_estim > 2: 
                print('Warning, LR parameter has weird estimation: {}'.format(estim_param[0]))
            
            # store the best fitting parameter(s) in the estimation_DFs in the correct column (n_trials) and 
                # correct row (this_rep)
            
            LREstimation_DF.loc[pp, str(n_trials)] = np.round(estim_param[0], 3)
            TempEstimation_DF.loc[pp, str(n_trials)] = np.round(estim_param[1], 3)
    
    # Save the estimations 
    LREstimation_DF.to_csv(LREstimation_file)
    TempEstimation_DF.to_csv(TempEstimation_file)
