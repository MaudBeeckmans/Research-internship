# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:22:00 2021

@author: Maud
"""

from Functions_EEG_experiment import generate_parameters
import numpy as np 

all_possible_LR =False

if all_possible_LR == False: 
    N_pp = 80
    group_mean = 0.8
    group_std = 0.1
    Output_file = 'pp_overview{}_group1.csv'.format(N_pp)

    learning_rates = generate_parameters(mean = group_mean, std = group_std, n_pp = N_pp)
    pp_numbers = np.arange(0, N_pp, 1)
    size_array = N_pp
else: 
    learning_rates = np.arange(0, 1.1, 0.1)
    size_array = learning_rates.shape[0]
    pp_numbers = np.arange(0, size_array, 1)
    Output_file = 'allLR_overview.csv'

learning_rates = np.round(learning_rates, 3)
data_selection = np.random.randint(0, 10, size = size_array)


CSV = np.column_stack([learning_rates, data_selection, pp_numbers])
np.savetxt(Output_file, CSV, delimiter = ',', fmt = ("%.3f", "%.i", "%.i"),
              header = 'LR,Data,pp', comments = '')

