# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:06:10 2021

@author: Maud
"""

from Functions_EEG_experiment import simulate_RW
import pandas as pd 
import sys, os
import numpy as np 

HPC = False
n_pp = 80

if HPC == True:
    params = sys.argv[1:]   #Get the params from another file (in CSV file)
    assert len(params) == 3     #Checks whether there are 3 params
    # assign to some parameters
    LR, design_filename, pp_number = sys.argv[1:]
    LR = np.float(LR)
    design_filename = int(design_filename)
    design_filename = 'Data{}.csv'.format(str(design_filename))
    pp_number = int(pp_number)
    Output_folder = os.path.join(os.environ.get('VSC_SCRATCH'), 'RW_EEG', 'Simulations', 'Participant{}'.format(str(pp_number)))
    if not os.path.isdir(Output_folder): 
            os.makedirs(Output_folder)
    Design_file = os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', design_filename)
    nreps = 2    #for each pp. generate 1000 'experiment-executions' 
    for rep in range(nreps): 
        Output_file = os.path.join(Output_folder, 'participant{}rep{}.csv'.format(str(pp_number), str(rep)))
        total_reward = simulate_RW(learning_rate = LR, design_file = Design_file, output_file = Output_file)
        print(total_reward)


else: 
    for pp in range(n_pp): 
        print("We're at pp {}".format(pp))
        DF = pd.read_csv('pp_overview.csv')
        LR, design_filename, pp_number = DF.iloc[pp, :]
        pp_number = int(pp_number)
        design_filename = int(design_filename)
        design_filename = 'Data{}.csv'.format(str(design_filename))
        Design_folder = r"C:\Users\Maud\Documents\Psychologie\2e master psychologie\Research Internship\Start to model RI\Maud_Sims\RW\Data_to_fit"
        Design_file = os.path.join(Design_folder, design_filename)
        Output_folder = os.path.join(os.getcwd(), 'Simulations', 'Participant{}'.format(str(pp_number)))
        nreps = 20
        reps = np.arange(0, nreps, 1)
        if not os.path.isdir(Output_folder): 
            os.makedirs(Output_folder)
        for rep in reps: 
            Output_file = os.path.join(Output_folder, 'participant{}rep{}.csv'.format(str(pp_number), str(rep)))
            total_reward = simulate_RW(learning_rate = LR, design_file = Design_file, output_file = Output_file)
            print(total_reward)
        
    


