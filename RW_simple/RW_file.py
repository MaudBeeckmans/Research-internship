# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 11:38:20 2021

@author: Maud
"""

from Simulate_data import generate_parameters, simulate_data
from Estimate_likelihood import likelihood
import numpy as np
import pandas as pd
import os 
import sys
from scipy import optimize


"""Now possible to make a dataframe with the estimations for all participants!"""

HPC = True


# # get identifier of the datafile you want to process
# if HPC == True: 
#     val = sys.argv[1:]
#     assert len(val) == 1
#         #length 1 since only 1 parameter now 
#     pp = val[0]
# else: 
#     pp = 1

#%%

if HPC == True: 
    data_dir = os.environ.get('VSC_SCRATCH')
    simul_dir = data_dir + '/RW_simple/Data'
else: 
    simul_dir= os.getcwd()

N_pp = 40
participants = np.arange(0, N_pp, 1).astype(int)
trials = np.array([100, 200, 300, 500, 1000, 3000])
estimation_DF = pd.DataFrame(columns = np.concatenate([['real_param'], trials.astype(str)]))
for pp in participants: 
    Parameters = pd.DataFrame(columns = ['n_trials', 'alpha_estimate', 'temp_estimate', 
                                         'alpha_real', 'temp_real'])
    data_file = simul_dir + str('/Simulation_pp{}.csv'.format(pp))
    data = pd.read_csv(data_file)
    alpha_real = data['learning_rate'][0]   #what was the actual learning rate of the pp. 
    estimation_DF = estimation_DF.append({'real_param': alpha_real}, ignore_index = True)
        #add the real learning rate to the array 
    pos = 1
    for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
        estim_param = optimize.fmin(likelihood, np.random.rand(1), args =(tuple([data_file, n_trials])), 
                                maxiter= 100000, ftol = 0.001)
            #gradient descent function to find the most likely parameters given the data 
                #might have to repeat this several times 
        alpha_estimate = estim_param #the most likely learning rate, given the data 
        print('real alpha is {}, estimated alpha is {}'.format(alpha_real, alpha_estimate))
        estimation_DF.iloc[pp, pos] = np.round(alpha_estimate, 3)
        pos = pos + 1
estimation_DF.to_csv(data_dir + '/RW_simple' + '/Estimations.csv')
