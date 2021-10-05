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

HPC = False
import_power = True 

mean_group1 = 0.4
mean_group2 = 0.7
general_std = 0.2
n_pp = 20

if import_power == False or HPC == True: 
    p_values_group1, data_group1 = simulate_tosses(Mean_prob = mean_group1, Std_prob = general_std, 
                                                   N_trials = 10000, N_pp = int(n_pp/2))
    p_values_group2, data_group2 = simulate_tosses(Mean_prob = mean_group2, Std_prob = general_std, 
                                                   N_trials = 10000, N_pp = int(n_pp/2))
    data_all_pp = np.row_stack([data_group1, data_group2])
    all_p_values = np.concatenate([p_values_group1, p_values_group2])

"""When generating 10 000 trials, the mean is not exactly equal to the proposed mean, 
this is probably due to the cut-off at 0 and 1, thus a bit skewed normal distribution"""




#%%

import scipy.stats as stat
import pandas as pd 

n_reps = 10000
# all_used_trials = [5, 10, 100, 500, 1000]
if HPC == True or import_power == True: 
    all_used_trials = np.arange(5, 105, 5)
else: 
    all_used_trials = [5]
cut_off_A = 0.9       #formula: cor(p, p_estimates) > 0.8 with n_pp participants
cut_off_B = 0.05

power_A = 'Power_corr' + str(cut_off_A)
power_B = 'Power_signif_diff'

if import_power == False: 
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

if import_power == True: 
    power_dataframe = pd.read_csv("Coin_tossPower_df_corr0.9_20ppB.csv")
else: 
    filename = target_dir + 'Power_df_corr0.9_20pp.csv'
    power_dataframe.to_csv(filename)
    
    

#%%

"""When running script on the HPC this part should be commented!"""
if HPC != True: 
    from matplotlib import pyplot as plt 
    power_options = [power_A, power_B]
    fig, axes = plt.subplots(nrows = 2, ncols = 1)
    for i in range(2): 
        axes[i].plot(power_dataframe['n_trials'], power_dataframe[power_options[i]], "ro")
        axes[i].set_ylim([0, 1.1])
        axes[i].set_xlim([0, max(all_used_trials) + 10])
        axes[i].set_xlabel('N_trials', loc = 'right')
        y_label = axes[i].set_ylabel('P', loc = 'top')
        y_label.set_rotation(0)
    axes[0].set_title("{} pp, power = P(corr(p_est, p) > {})".format(n_pp, cut_off_A))
    axes[1].set_title("{} pp, power = P(pgroup1 < pgroup2) p-value <= {}".format(n_pp, cut_off_B))
    
    fig.savefig('Power.png')



"""

* met 50 pp: correlatie al vanaf 10 trials altijd boven de 80%, dus power = 100% 
* met 20 pp: power bij 10 trials is 93,18%; 99,13%; 98,8% voor cut-off = 0.8
* met 10 pp: power bij 10 trials is - 94,54% voor cut-off = 0.8
                                    - 57.32%, 57.11% voor cut-off = 0.9


Remark: als er teveel p = 0 of p = 1 zijn, dan zal dit de correlatie omhoog trekken, want dan 
is de p_estimate sowieso correct 
"""

