# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:22:51 2021

@author: Maud
"""

# params = sys.argv[1:]   #Get the params from another file (in CSV file)
# assert len(params) == 2     #Checks whether there are 3 params

import os
import numpy as np 
from Functions_actual_data import Value_PE_estimation
import pandas as pd
from scipy import stats

# Path to the datafile conatining the correct parameter estimates for all the participants
estimates = pd.read_csv(r"C:/Users/Maud/Documents/Psychologie/2e master psychologie/Research Internship/Start to model RI/Projects/RW_EEG/Estimations_realpp/Estimate_realpp_1param.csv")
incorrect_LR = 0.9 # a specific LR or 'None'
    # allows to create Value_ & PE_series with an incorrect LR; has to be 'None' if we want to use the correct estimates 

#Create folders that will contain the Value_ and PE_series for all participants given the current (correct or incorrect LR)
Value_folder = os.path.join(os.getcwd(), 'Value_series')
PE_folder = os.path.join(os.getcwd(), 'PE_series')
if not os.path.isdir(Value_folder): 
    os.mkdir(Value_folder)
if not os.path.isdir(PE_folder):
    os.mkdir(PE_folder)

# Create the Value & PE series for each participants and store these in separate arrays 
    # One array will contain the Value_series for all pp.; one array will contain the PE_series for all pp. 
for i in range(estimates.shape[0]):# estimates.shape[0] = the number of pp. 
    pp = estimates.iloc[i, 0] # first column of this dataframe contains the participant number (!! to find the correct design)
    # if-else: defines which LR to use; if the correct one should be used, this is drawn from the estimate DF
    if incorrect_LR == None: parameters = estimates.iloc[i, 1]
    else: parameters = [incorrect_LR]
    
    # in the Value_PE_estimation function, parameter[0] is the LR and parameter[1] is the Temperature thus combine these into an array
    parameters = np.append(parameters, 0.41) #Temperature is fixed at 0.41 (this is the mean estimate in the paper)
    #design_file: contains the choices, responses etc. !! to deduce the Value_series and PE_series for this pp.
    design_file = os.path.join(os.getcwd(), 'Behavioral_Data', 'Probabilistic_Reversal_task_subject_{}_Session_0_data.tsv'.format(pp))
    # Value_PE_estimation: function to estimate the Value_ and PE_series given the currently used parameters 
    Value_series, PE_series, actual_rewards = Value_PE_estimation(parameters, design_file, 480)
    
    if i == 0: # creates the big arrays that will containt the Value_ or PE_series for all pp. (shape = n_pp x n_trials)
        all_values = Value_series
        all_PEs = PE_series
        all_rewards = actual_rewards
    else: 
        all_values = np.row_stack([all_values, Value_series])
        all_PEs = np.row_stack([all_PEs, PE_series])
        all_rewards = np.row_stack([all_rewards, actual_rewards])

# Delete some variables to clean the variable explorer 
del design_file, estimates, i, PE_folder, PE_series, Value_folder, Value_series, pp, actual_rewards

#%% Correlate the Value_series & PE_series with the theta-power recordings for each participant

# Create empty arrays that will contain the P_values and correlations for each participant 
P_values = np.array([])
correlations = np.array([])
# load the file containing the theta-amplitude recordings for all pp. at each trial (shape = n_pp x n_trials)
theta_power = pd.read_csv(r'file:///C:/Users/Maud/Documents/Psychologie/2e master psychologie/Research Internship/Start to model RI/Projects/RW_EEG/Behavioral_Data/Theta_power.csv', header = None)
# Calculate the correlation and significance of the correlation for each participant 
for i in range(theta_power.shape[0]): #theta_power.shape[0] = the number of participants 
    
    # select the relevant arrays for the correlation
    this_theta = theta_power.iloc[i, :].to_numpy()[:480] # select the relevant theta-series (the one for this pp.)
    this_PE = all_PEs[i, :][:480] # select the relevant PE_series (the one for this pp.)
    
    # Compute the correlation and significance of the correlation for this pp. 
    corr, P_value = stats.spearmanr(this_theta, np.abs(this_PE), nan_policy = 'omit')
    
    #Store  the correlations and the P_values 
    correlations = np.append(correlations, corr)
    P_values = np.append(P_values, P_value)

#Create an extra array indicating whether the correlation was significant or not with cut-off = 0.05
significance = np.where(P_values < 0.05, 1, 0)

#Create a array with 3 rows containing the correlations, P_values and significance of the correlations for all pp. 
corr_P = np.column_stack([correlations, P_values, significance])

# Store the above array as a csv-file
# np.savetxt('Correlations_absolutePEandTheta_LR{}.csv'.format(parameters[0]), 
#            corr_P, header = 'corr,P_value,significance', fmt = '%.4f', delimiter = ',')

# Delete some variables to clean the variable explorer 
del i, corr, P_value, P_values, correlations, significance, this_PE, this_theta

