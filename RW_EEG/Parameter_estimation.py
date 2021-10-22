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


group = 1 #when using allLR, put group to 'allLR'
trials =  np.array([50, 100, 200, 300, 480, 480*2, 480*3]) #The number of trials that will be used to estimate the parameter(s)
used_reps = 100 # The number of repetitions per participant that will be used to estimate the parameter(s)
used_temperature = 0.41

if group == 'allLR': N_simulations = 11
else: N_simulations = 80


# Define for which simulation we'll currently do the estimations at each repetition with each possible number of trials in trials used for the estimation
simul_number = sys.argv[1:] #Get the params from another file (in CSV file)
print(simul_number)
assert len(simul_number) == 1     #Checks whether there are n params
simul = int(simul_number[0])


# Define the name of the folder that contains the necessary input variables
#Which_design: from the overview file, see which design_file was used to simulate the data of this simulation
    #.iloc[a, b]: a = the row corresponding to this simulation number, b = the column containing the number of the design file used for this simulation
which_design = pd.read_csv('pp_overview{}_group{}.csv'.format(N_simulations, group)).iloc[simul, 1] 
start_design = pd.read_csv(os.path.join(os.getcwd(), 'Design', 'Data{}.csv'.format(which_design)))
# the trials within the design were repeated three times when simulating the responses (shape = 1440 x 10)
start_design = start_design.append(start_design).append(start_design)
#Get the correct responses from the responses_file (shape = 1000x1440)
responses_allreps = pd.read_csv(os.path.join(r'/kyukon/scratch/gent/442/vsc44254/RW_EEG/Responses_group{}'.format(group), 
                                             'Responses_simulation{}.csv'.format(simul)), header = None)
responses_allreps = np.array(responses_allreps)

# Define the name of the folder that will contain the estimations for each simulation within this group
estim_folder = 'Estimations_group{}'.format(group) # Folder name
Estimation_folder = os.path.join(r'/kyukon/scratch/gent/442/vsc44254/RW_EEG/', estim_folder) # Complete path 

# Create the folder that will contain the estimations for this group (1 file per simulation)
if not os.path.isdir(Estimation_folder):
    os.makedirs(Estimation_folder)


# Create the file (with path) to which the estimation_DF will be written eventually 
Estimation_file = os.path.join(Estimation_folder, 'Estimate_pp{}.csv'.format(simul))
# Create the dataframe that will contain all the estimations for this simulation (shape will be: n_reps x n_cols)
estimation_DF = pd.DataFrame(columns = np.concatenate([['real_param'], trials.astype(str), ['rep']]))

# Do the estimation over all repetitions for this simulation 
for this_rep in range(used_reps): 
    # Combine the start_design of this simulation and the responses given within this repetition
    start_design['Response'] = responses_allreps[this_rep, :]
    # Create some space to fill in the estimation_DF 
    estimation_DF = estimation_DF.append({'rep': this_rep}, ignore_index = True)
    for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
        # estimate the parameters given the start_design; n_trials defines how many trials are used to estimate the parameter(s) 
        estim_param = optimize.fminbound(likelihood, 0, 1, args =(tuple([start_design, n_trials, used_temperature])), 
                            maxfun= 100000, xtol = 0.001)
        # store the best fitting parameter(s) in the estimation_DF in the correct column (n_trials) and correct row (this_rep)
        estimation_DF[str(n_trials)][this_rep] = estim_param

# Save the estimations 
estimation_DF.to_csv(Estimation_file)
