# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 12:40:57 2021

@author: Maud
"""

from Coin_toss_simulation import generate_tosses, simulate_tosses
from Coin_toss_estimation import estimate_p_tails
import numpy as np
from scipy.stats import pearsonr
import os 
import pandas as pd
import scipy.stats as stat
import pandas as pd 

HPC = True
fix_simulations = True

letters = ['A', 'B', 'C', 'D']
letters = ['Z']
for letter in letters: 
    imported_data = 'simulated_data' + letter + '.csv'
    imported_p = 'p_simulations' + letter + '.csv'
    mean_group1 = 0.4
    mean_group2 = 0.7
    general_std = 0.2
    n_pp = 80
    if fix_simulations == False: 
        if fix_simulations == False: 
            p_values_group1, data_group1 = simulate_tosses(Mean_prob = mean_group1, Std_prob = general_std, 
                                                           N_trials = 10000, N_pp = int(n_pp/2))
            p_values_group2, data_group2 = simulate_tosses(Mean_prob = mean_group2, Std_prob = general_std, 
                                                           N_trials = 10000, N_pp = int(n_pp/2))
            data_all_pp = np.row_stack([data_group1, data_group2])
            all_p_values = np.concatenate([p_values_group1, p_values_group2])
            # pd.DataFrame(data_all_pp).to_csv("simulated_data" + letter + ".csv", header = None, index = None)
            # pd.DataFrame(all_p_values).to_csv("p_simulations" + letter + ".csv", header = None, index = None)
    else: 
        print('Simulations imported')
        data_all_pp = pd.read_csv(imported_data, header = None)
        data_all_pp = data_all_pp.values
        all_p_values = pd.read_csv(imported_p, header = None)
        all_p_values = all_p_values.values
        all_p_values = all_p_values.reshape(n_pp)
    
    """When generating 10 000 trials, the mean is not exactly equal to the proposed mean, 
    this is probably due to the cut-off at 0 and 1, thus a bit skewed normal distribution"""
    
    #Power estimation for this dataset (1 dataset = n_pp and 10 000 trials per participant)
    n_reps = 10000
    # all_used_trials = [5, 10, 100, 500, 1000]
    if HPC == True: 
        all_used_trials = np.arange(5, 105, 5)
    else: 
        all_used_trials = [5]
    cut_off_A = 0.9       #formula: cor(p, p_estimates) > 0.8 with n_pp participants
    cut_off_B = 0.05
    
    power_A = 'Power_corr' + str(cut_off_A)
    power_B = 'Power_signif_diff'
    

    power_dataframe = pd.DataFrame(columns = ["n_trials", power_A, power_B])
    for current_ntrials in all_used_trials: 
        correlations = np.array([])
        P_values = np.array([])
        for rep in range(n_reps): 
            p_estimates = estimate_p_tails(N_used_trials = current_ntrials, N_pp = n_pp, Data = data_all_pp)
            correlation, _ = pearsonr(p_estimates, all_p_values)
            #correlations: array that in the end holds 10 000 values, one correlation per repetition
            correlations = np.append(correlations, correlation)
            #Now: 2-sided p-value! 
            T_stat, P_value = stat.ttest_ind(p_estimates[:int(n_pp/2)], p_estimates[int(n_pp/2):])
            P_values = np.append(P_values, P_value)
            if rep%1000 == 0: 
                print("We're at repetition number {}".format(rep))
        powerA = np.mean(np.where(correlations > cut_off_A, 1, 0))
        powerB = np.mean(np.where(P_values <= 0.05, 1, 0))
        print("P(cor(p, p_est) > {} with {} pp and {} trials is {}".format(cut_off_A, n_pp, current_ntrials, powerA))
        print("P(pgroup1 < pgroup2) and p-value <= {} with {} pp and {} trials is {}".format(cut_off_B, n_pp, current_ntrials, powerB))
        power_dataframe = power_dataframe.append({'n_trials': current_ntrials, power_A: powerA, power_B: powerB}, 
                                                 ignore_index = True)
        if powerA > 0.9 and powerB > 0.9: 
            break 
    print(all_p_values)

    if HPC == True: 
        data_dir = os.environ.get('VSC_DATA')
        target_dir = data_dir + '/Coin_toss'
        if not os.path.isdir(target_dir): 
            os.mkdir(target_dir)
    else: 
        target_dir = os.getcwd()
    
    filename = target_dir + '/Power_df_20pp' + letter + '.csv'
    power_dataframe.to_csv(filename)
        
