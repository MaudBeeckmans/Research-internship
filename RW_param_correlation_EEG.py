# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:31:59 2021

@author: Maud
"""

"""This version: 
- both in simulations and in the PE & V computation with incorrect learning rate, weights starting all at 0.5
- for each ground_truth lerning rate a simulation was created (RWsimulation_EEGexp script)
- for each simulated data (thus each ground truth learning rate), the values & PEs are counted if each of the other
learning rates to be used incorrectly for the analysis 
  --> correlations are then computed corr(true_values, incorrect_values) and corr(true_PEs, incorrect_PEs)
  --> all the correlatons are stored in a matrix (rows = true_learning_rates, columns = incorrect_learning_rates, 
                                                     cells = correlations)
      (1 matrix for the correlations of the values and one for the correlations of the PEs)
- now: trying to plot the correlations as well 
 """

import numpy as np
import pandas
from psychopy import data , os
from Simple_RW_model import softmax, choose_option, rescorla_wagner
from matplotlib import pyplot as plt
from scipy.stats import pearsonr

#learning_rates are rounded, otherwise something weird happens at learning rates 0.1*k (with k = constante)
learning_rates = np.round(np.arange(0.01, 1, 0.01), 2)
data_path = os.path.join(os.getcwd(), "Simulating_first_try")
def select_data(true_learning_rate = 0.01):
    selectA = np.where(learning_rates == true_learning_rate)[0][0]
    dataA = pandas.read_csv(os.path.join(data_path, "Simulation_" + str(selectA) + '.csv'))
    n_trials = dataA.shape[0]
    #first for the variance
    return dataA, n_trials

def generate_data_incorrect_alpha(design = None, incorrect_learning_rate = 0.02): 
    # weights = np.zeros(shape = (2, 2))
    weights = np.array([[0.5, 0.5], [0.5, 0.5]])
    PE_each_trial = np.array([])
    Expected_value_each_trial = np.array([])
    for trial in range(n_trials): 
        stimulus = np.int(design.iloc[trial, 2])
        response = np.int(design.iloc[trial, 3])
        CorResp =  np.int(design.iloc[trial, 4])
        FBcon = np.int(design.iloc[trial, 5])
        
        Expected_value = weights[stimulus, response]
        
        reward_present = ((response == CorResp and FBcon == 1) or (response != CorResp and FBcon == 0))*1
        PE, update_value = rescorla_wagner(previous_value = weights[stimulus, response], 
                        obtained_rew = reward_present, learning_rate = incorrect_learning_rate)
        PE_each_trial = np.append(PE_each_trial, PE)
        Expected_value_each_trial = np.append(Expected_value_each_trial, Expected_value)
        
        weights[stimulus, response] = update_value
        
    return PE_each_trial, Expected_value_each_trial

correlations_PE = np.empty(shape = (learning_rates.size, learning_rates.size))
correlations_V = np.empty(shape = (learning_rates.size, learning_rates.size))

for i in range(learning_rates.shape[0]): 
    true_alpha = learning_rates[i]
    dataA, n_trials = select_data(true_learning_rate = true_alpha)
    PE_dataA = dataA['PE_estimate']
    Value_dataA = dataA['Expected value']
    for j in range(learning_rates.shape[0]): 
        used_alpha = learning_rates[j]
        PE_dataB, Value_dataB = generate_data_incorrect_alpha(design = dataA, incorrect_learning_rate = used_alpha)
        #plt.scatter(PE_dataA, PE_dataB)
        corr_PE, _ = pearsonr(PE_dataA, PE_dataB)
        corr_V, _ = pearsonr(Value_dataA, Value_dataB)
        correlations_PE[i, j] = corr_PE
        correlations_V[i, j] = corr_V
        print(corr_PE, corr_V)
        
    #Store corr_PE and corr_V in the matrix 

    
