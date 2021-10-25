# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:22:00 2021

@author: Maud
"""

from Functions_EEG_experiment import generate_parameters
import numpy as np 

group = 3
variable_Temps = True

if group != 'allLR': 
    N_simulations = 80
    group_mean = 0.7
    group_std = 0.1
    learning_rates = generate_parameters(mean = group_mean, std = group_std, n_pp = N_simulations)
else: 
    learning_rates = np.arange(0, 1.1, 0.01)
    N_simulations = learning_rates.shape[0]
if variable_Temps == True: temperatures = generate_parameters(mean = 0.6, std = 0.2, n_pp = N_simulations)
else: temperatures = np.repeat(0.41, N_simulations)

Output_file = 'pp_overview{}_group{}_variableTemp.csv'.format(N_simulations, group)
simul_numbers = np.arange(0, N_simulations, 1)
    
learning_rates = np.round(learning_rates, 3)
temperatures = np.round(temperatures, 3)
data_selection = np.random.randint(0, 10, size = N_simulations)


CSV = np.column_stack([learning_rates, temperatures, data_selection, simul_numbers])
np.savetxt(Output_file, CSV, delimiter = ',', fmt = ("%.3f","%.3f", "%.i", "%.i"),
              header = 'LR,Temp,Data,pp', comments = '')
