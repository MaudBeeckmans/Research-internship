# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:51:03 2021

@author: Maud
"""

import numpy as np
from scipy.stats import pearsonr

def estimate_p_tails(N_used_trials = 10, N_pp = 25, Data = None): 
    p_estimates = np.array([])
    for pp in range(N_pp): 
        selected_trials = np.random.choice(Data[pp, :], N_used_trials)
        estimated_p = np.mean(selected_trials)
        p_estimates = np.append(p_estimates, estimated_p)
    return p_estimates 


"""Part below is commented, since this is now implemented in the coin_toss script itself"""
# def power_optionA(n_reps = 1000, n_trials = 10, n_pp = 25, trial_data = None, target_p = None): 
#     correlations = np.array([])
#     for rep in range(n_reps): 
#         p_estimates = estimate_p_tails(n_T = n_trials, n_participants = n_pp, data = trial_data)
#         correlation, _ = pearsonr(p_estimates, target_p)
#         correlations = np.append(correlations, correlation)
#     return correlations 
        
                
        
