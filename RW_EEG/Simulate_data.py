# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:06:10 2021

@author: Maud
"""

from Functions_EEG_experiment import simulate_RW
import pandas as pd 
import sys, os
import numpy as np 


nreps = 100          #for each pp. generate 1000 'experiment-executions' 
group = 1 #when using allLR, put group to 'allLR'
temp_type = 'variable' # should be variable or fixed

if group == 'allLR': 
    output_folder = 'Simulations_all_LR'

else: 
    output_folder = 'Simulations_group{}_Temp{}'.format(group, temp_type)


params = sys.argv[1:]   #Get the params from another file (in CSV file)
assert len(params) == 4     #Checks whether there are 3 params
# assign to some parameters
LR, Temp, design_filename, pp_number = sys.argv[1:]
LR = np.float(LR)
Temp = np.float(Temp)
design_filename = int(design_filename)
design_filename = 'Data{}.csv'.format(str(design_filename))
pp_number = int(pp_number)
Output_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG', output_folder)
if not os.path.isdir(Output_folder): 
        os.makedirs(Output_folder)
Design_file = os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', design_filename)

for rep in range(nreps): 
    total_reward, responses = simulate_RW(learning_rate = LR, design_file = Design_file, temperature = Temp, 
                                          triple_trials = True)
    if rep == 0: store_responses = responses
    else: store_responses = np.row_stack([store_responses, responses])

Output_file = os.path.join(Output_folder, 'Simulation{}.csv'.format(str(pp_number)))
np.savetxt(Output_file, store_responses, fmt = '%.i', delimiter = ',') 
