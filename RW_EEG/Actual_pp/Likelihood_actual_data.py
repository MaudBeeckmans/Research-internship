# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:49:34 2021

@author: Maud
"""
import pandas as pd
import numpy as np
from Functions_realdata import likelihood_realdata
import os
from scipy import optimize



folder = os.path.join(os.getcwd(), 'Behavioral_Data') #Folder containing the participant files
n_pp = 34 #total number of participants
n_params = 2 # number of estimated parameters
participants = np.arange(1, n_pp+1, 1) #range of participant numbers used in the participant file_names
trials = 480 # number of trials used to estimate the learning rate (480 is max since only data on 480 trials)

# create dataframe that will contain the estimates of the 1 or 2 parameters for each participant
if n_params == 1: column_name = ['LR']
else: column_name = ['LR', 'Temp']
estimation_DF = pd.DataFrame(columns = column_name, 
                             index = participants)

# Create folder to store the estimations for all participants 
Estimation_folder = os.path.join(os.getcwd(), 'Estimations_realpp')
if not os.path.isdir(Estimation_folder):
    os.mkdir(Estimation_folder)
#Estimation_file: file that will eventually contain the estimates for all the participants 
Estimation_file = os.path.join(Estimation_folder, 'Estimate_realpp_{}param.csv'.format(n_params))

# Loop over each participant to estimate the parameter(s) for each participant 
for pp in participants: 
    print("We're at pp {}".format(pp)) # keep track of where we are within all the participants 
    # file_name: contains path towards the file containing the behavioural data of this participant 
    file_name = os.path.join(folder, 
                "Probabilistic_Reversal_task_subject_{}_Session_0_data.tsv".format(pp))
    #Estimate the parameter(s) using one of 2 methods
    # Method 1: optimize.fmin - does not always find the appropriate parameters 
    # estim_param = optimize.fmin(likelihood_realdata, np.random.rand(2), 
    #                                   args =(tuple([file_name, n_trials])), 
    #                                   maxfun= 100000, xtol = 0.001)
    
    # Method 2: differential evolution - gives more accurate estimations, but takes longer 
    estim_param2 = optimize.differential_evolution(likelihood_realdata, [(0,1), (-10, 10)], args = (tuple([file_name, trials])), 
                                              maxiter = 100000, tol = 0.005)
    estim_param = estim_param2.x
    print(estim_param)
    
    #Store the estimated LR and Temperature for this participant in the estimation_dataframe
    estimation_DF['LR'][pp] = estim_param[0]
    estimation_DF['Temp'][pp] = estim_param[1]

# for these participants, the EEG data was correctly recorded; thus only keep the estimates for these participants
pp_to_keep = np.array([3, 5, 6, 7, 9, 10, 12, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34])
estimation_DF = estimation_DF.iloc[pp_to_keep-1]

# Write the estimation_DF to a csv-file
estimation_DF.to_csv(Estimation_file)

