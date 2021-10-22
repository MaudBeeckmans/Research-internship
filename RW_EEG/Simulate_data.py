# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:06:10 2021

@author: Maud
"""

from Functions_EEG_experiment import simulate_RW
import pandas as pd 
import sys, os
import numpy as np 


nreps = 1000            #for each pp. generate 1000 'experiment-executions' 
group = 3 #when using allLR, put group to 'allLR'

if group == 'allLR': 
    output_folder = 'Simulations_all_LR'
    csv_file = 'allLR_overview.csv'

else: 
    output_folder = 'Simulations_group{}'.format(group)
    csv_file = 'pp_overview80_group{}.csv'.format(group)


params = sys.argv[1:]   #Get the params from another file (in CSV file)
assert len(params) == 3     #Checks whether there are 3 params
# assign to some parameters
LR, design_filename, pp_number = sys.argv[1:]
LR = np.float(LR)
design_filename = int(design_filename)
design_filename = 'Data{}.csv'.format(str(design_filename))
pp_number = int(pp_number)
Output_folder = os.path.join(os.environ.get('VSC_SCRATCH'), 'RW_EEG', output_folder, 
                             'Simulation{}'.format(str(pp_number)))
if not os.path.isdir(Output_folder): 
        os.makedirs(Output_folder)
Design_file = os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', design_filename)

for rep in range(nreps): 
    Output_file = os.path.join(Output_folder, 'Simulation{}rep{}.csv'.format(str(pp_number), str(rep)))
    total_reward = simulate_RW(learning_rate = LR, design_file = Design_file, 
                               output_file = Output_file, triple_trials = True)
    print(rep)
