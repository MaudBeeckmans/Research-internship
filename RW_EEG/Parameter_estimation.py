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

HPC = False 
if HPC == True:
    pp_number = sys.argv[1] #Get the params from another file (in CSV file)
    print(len(pp_number))
    # assert len(pp_number) == 1     #Checks whether there are n params
    folder_simul_name = os.path.join('/kyukon/scratch/gent/442/vsc44254/RW_EEG/Simulations', 
                                     'Participant{}'.format(pp_number))
    Estimation_folder = r'/kyukon/scratch/gent/442/vsc44254/RW_EEG/Estimations'
    if not os.path.isdir(Estimation_folder): 
        os.makedirs(Estimation_folder)
    Estimation_file = os.path.join(Estimation_folder, 'Estimate_pp{}.csv'.format(pp_number))
else: 
    participants = np.arange(0, 80, 1)
    for pp_number in participants:   
        print("We're at pp {}".format(pp_number))
        folder_simul_name = os.path.join(os.getcwd(), 'Simulations', 'Participant{}'.format(pp_number))    
        simul_files = os.listdir(folder_simul_name)
        Estimation_folder = os.path.join(os.getcwd(), 'Estimations')
        if not os.path.isdir(Estimation_folder):
            os.makedirs(Estimation_folder)
        Estimation_file = os.path.join(Estimation_folder, 'Estimate_pp{}.csv'.format(pp_number))
        trials = np.array([100, 200, 300, 400, 480])
        estimation_DF = pd.DataFrame(columns = np.concatenate([['real_param'], trials.astype(str), ['rep']]))
        
        for simul_file in simul_files: 
            file_name = os.path.join(folder_simul_name, simul_file)
            estimation_DF = estimation_DF.append({'rep': file_name}, ignore_index = True)
            for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
                # print('\n {}'.format(n_trials))
                estim_param = optimize.fminbound(likelihood, 0, 1, args =(tuple([file_name, n_trials])), 
                                    maxfun= 100000, xtol = 0.001)
                estimation_DF[str(n_trials)][int(simul_file[-5])] = estim_param
        estimation_DF.to_csv(Estimation_file)

if HPC == True: 
    simul_files = os.listdir(folder_simul_name)
    
    trials = np.array([100, 200, 300, 400, 480])
    estimation_DF = pd.DataFrame(columns = np.concatenate([['real_param'], trials.astype(str), ['rep']]))
    
    for simul_file in simul_files: 
        file_name = os.path.join(folder_simul_name, simul_file)
        estimation_DF = estimation_DF.append({'rep': file_name}, ignore_index = True)
        for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
            # print('\n {}'.format(n_trials))
            estim_param = optimize.fminbound(likelihood, 0, 1, args =(tuple([file_name, n_trials])), 
                                maxfun= 100000, xtol = 0.001)
            estimation_DF[str(n_trials)][int(simul_file[-5])] = estim_param
    estimation_DF.to_csv(Estimation_file)
            # print('estimated alpha: {}'.format(estim_param))
        
    
    
