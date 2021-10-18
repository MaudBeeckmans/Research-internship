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

HPC = True 
all_possible_LR = False

if all_possible_LR == True: 
    N_simulations = 11
    simul_folder = os.path.join('Final_simul_est_files', 'Simulations_all_LR')
    estim_folder = 'Estimations_all_LR'
else: 
    N_simulations = 80
    simul_folder = 'Simulations_group1'
    estim_folder = 'Estimations_group1'


trials =  np.array([50, 100, 200, 300, 480, 480*2, 480*3])
used_reps = 1000
# trials = np.array([100, 200, 300, 400, 480])


if HPC == True:
    simul_number = sys.argv[1:] #Get the params from another file (in CSV file)
    print(simul_number)
    assert len(simul_number) == 1     #Checks whether there are n params
    simul_number = simul_number[0] 
    folder_simul_name = os.path.join('/kyukon/scratch/gent/442/vsc44254/RW_EEG/', simul_folder, 
                                     'Simulation{}'.format(simul_number))
    Estimation_folder = os.path.join(r'/kyukon/scratch/gent/442/vsc44254/RW_EEG/', estim_folder)
    simulations = [simul_number]
else: 
    simulations = np.arange(0, N_simulations, 1)
    Estimation_folder = os.path.join(os.getcwd(), estim_folder)


if not os.path.isdir(Estimation_folder):
    os.makedirs(Estimation_folder)

for simul in simulations:   
    print("We're at simulation {}".format(simul))
    if HPC == False: 
        folder_simul_name = os.path.join(os.getcwd(), simul_folder, 'Simulation{}'.format(simul))    
    # simul_files = os.listdir(folder_simul_name)#Not used anymore since this doesn't give the correctorder!
    Estimation_file = os.path.join(Estimation_folder, 'Estimate_pp{}.csv'.format(simul))
    estimation_DF = pd.DataFrame(columns = np.concatenate([['real_param'], trials.astype(str), ['rep']]))
    
    file_count = 0 #keep track of the file number we're currently at
    simul_files = []
    for i in range(used_reps): simul_files = np.append(simul_files, "Simulation{}rep{}.csv".format(simul, i))
    print(simul_files)
    for simul_file in simul_files: 
        file_name = os.path.join(folder_simul_name, simul_file)
        estimation_DF = estimation_DF.append({'rep': file_count}, ignore_index = True)
        for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
            # print('\n {}'.format(n_trials))
            estim_param = optimize.fminbound(likelihood, 0, 1, args =(tuple([file_name, n_trials])), 
                                maxfun= 100000, xtol = 0.001)
            estimation_DF[str(n_trials)][file_count] = estim_param
        file_count += 1
    estimation_DF.to_csv(Estimation_file)


   
