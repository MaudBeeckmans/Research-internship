# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:31:59 2021

@author: Maud
"""

"""Incorrect version!
   - now var-cov matrix is computed of the PEs that are computed with different choices made 
   - should look at the choices made by a real subject (simulation) but update the PE and vallues with a different
       learning rate than that actual subject (simulation)"""

import numpy as np
import pandas
from psychopy import data , os
from Simple_RW_model import softmax, choose_option, rescorla_wagner

#learning_rates are rounded, otherwise something weird happens at learning rates 0.1*k (with k = constante)
learning_rates = np.round(np.arange(0.01, 1, 0.01), 2)
def select_data(learning_rate1 = 0.01, learning_rate2 = 0.02):
    selectA = np.where(learning_rates == learning_rate1)[0][0]
    selectB = np.where(learning_rates == learning_rate2)[0][0]
    dataA = pandas.read_csv("Simulation_" + str(selectA) + '.csv' )
    dataB = pandas.read_csv("Simulation_" + str(selectB) + '.csv' )
    n_trials = dataA.shape[0]
    #first for the variance
    return dataA, dataB, n_trials


dataA, dataB, n_trials = select_data(learning_rate1 = 0.01, learning_rate2 = 0.02)
PE_dataA = dataA['PE_estimate']
PE_dataB = dataB['PE_estimate']
var_cov_matrix = np.cov(PE_dataA, PE_dataB)

    
    
    



    
    
    





