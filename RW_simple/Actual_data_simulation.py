# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:53:48 2021

@author: Maud
"""

from Simulate_data import generate_parameters, simulate_data
from Estimate_likelihood import likelihood
import numpy as np
import pandas as pd
import os 


HPC = True #Defines the correct directory to store the data 
test = False # should be True when testing on own laptop or in interactive qsub 
#%%Simulate data

if HPC == True: 
    data_dir = os.environ.get('VSC_SCRATCH')
    simul_dir = data_dir + '/RW_simple/Data'
    if not os.path.isdir(simul_dir):    #is not working!
        os.mkdir(simul_dir)
else: 
    simul_dir = os.getcwd()
#Mean groups copied from paper Katahiri & Totoyama 
mean_alpha1 = 0.4
mean_alpha2 = 0.2
std_alpha = 0.05
N_pp =40
N_trials = 10000
if test == True: 
    N_trials = 300
    N_pp = 2

learning_rates_G1 = generate_parameters(mean = mean_alpha1, std = std_alpha, n_pp = int(N_pp/2)) 
learning_rates_G2 = generate_parameters(mean = mean_alpha1, std = std_alpha, n_pp = int(N_pp/2))
Learning_rates = np.concatenate([learning_rates_G1, learning_rates_G2])
Temperatures = np.ones(N_pp)

DF_all_pp = simulate_data(learning_rates = Learning_rates, temperatures = Temperatures, 
                          n_trials = N_trials)

participants = np.arange(0, N_pp, 1).astype(int)
for pp in participants:
    DF_pp = pd.DataFrame(columns = ['trial', 'choices', 'rewards', 'temperature', 'learning_rate'])
    DF_pp['trial'] = np.arange(0, N_trials, 1)
    DF_pp['choices'] = DF_all_pp['choices'][pp]
    DF_pp['rewards'] = DF_all_pp['rewards'][pp]
    DF_pp['Value'] = DF_all_pp['Value_series'][pp]
    DF_pp['PE'] = DF_all_pp['PE_series'][pp]
    DF_pp['learning_rate'] = np.repeat(DF_all_pp['learning_rate'][pp], N_trials)
    DF_pp['temperature'] = np.repeat(DF_all_pp['temperature'][pp], N_trials)
    DF_pp.to_csv(simul_dir + '/Simulation_pp{}.csv'.format(pp))
