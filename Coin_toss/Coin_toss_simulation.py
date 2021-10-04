# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:34:19 2021

@author: Maud
"""

import numpy as np

def generate_tosses(N = 10, P_tails = 0.5): 
    tosses = [(np.random.random() <= P_tails)*1 for i in range(N)]
    return tosses
    
    
#volgende: één grote array met alle tosses in maken? Of een pandas dataframe

def simulate_tosses(Mean_prob = 0.5, Std_prob = 0.2, N_trials = 10, N_pp = 25):
    all_data = np.empty(shape = [N_pp, N_trials], dtype = int)
    p_values = np.round(np.random.normal(loc = Mean_prob, scale = Std_prob, size = N_pp), 3)
    p_values = np.where(p_values > 1, 1, p_values)
    p_values = np.where(p_values < 0, 0, p_values)
    for pp in range(N_pp): 
        tosses = generate_tosses(N = N_trials, P_tails = p_values[pp])
        all_data[pp, :] = tosses 
    return p_values, all_data


    
