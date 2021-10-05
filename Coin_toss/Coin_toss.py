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

mean_group1 = 0.4
mean_group2 = 0.7
general_std = 0.2
n_pp = 20


p_values_group1, data_group1 = simulate_tosses(Mean_prob = mean_group1, Std_prob = general_std, 
                                               N_trials = 10000, N_pp = int(n_pp/2))
p_values_group2, data_group2 = simulate_tosses(Mean_prob = mean_group2, Std_prob = general_std, 
                                               N_trials = 10000, N_pp = int(n_pp/2))

"""When generating 10 000 trials, the mean is not exactly equal to the proposed mean, 
this is probably due to the cut-off at 0 and 1, thus a bit skewed normal distribution"""


data_all_pp = np.row_stack([data_group1, data_group2])
all_p_values = np.concatenate([p_values_group1, p_values_group2])

#%%
import pandas as pd 

n_reps = 10000
# all_used_trials = [5, 10, 100, 500, 1000]
all_used_trials = np.arange(5, 105, 5)
cut_off = 0.9       #formula: cor(p, p_estimates) > 0.8 with n_pp participants

power_A = 'Power_corr' + str(cut_off)

power_dataframe = pd.DataFrame(columns = ["n_trials", power_A])
for current_ntrials in all_used_trials: 
    correlations = np.array([])
    for rep in range(n_reps): 
        p_estimates = estimate_p_tails(N_used_trials = current_ntrials, N_pp = n_pp, Data = data_all_pp)
        correlation, _ = pearsonr(p_estimates, all_p_values)
        #correlations: array that in the end holds 10 000 values, one correlation per repetition
        correlations = np.append(correlations, correlation)
        if rep%1000 == 0: 
            print("We're at repetition number {}".format(rep))
    power = np.mean(np.where(correlations > cut_off, 1, 0))
    print("P(cor(p, p_est) > {} with {} pp and {} trials is {}".format(cut_off, n_pp, current_ntrials, power))
    power_dataframe = power_dataframe.append({'n_trials': current_ntrials, power_A: power}, 
                                             ignore_index = True)

data_dir = os.environ.get('VSC_DATA')
target_dir = data_dir + '/Coin_toss'
if not os.path.isdir(target_dir): 
    os.mkdir(target_dir)

filename = target_dir + 'Power_df_corr0.9_20pp.csv'
power_dataframe.to_csv(filename)


#%%

"""When running script on the HPC this part should be commented!"""

power_dataframe = pd.read_csv("Coin_tossPower_df_corr0.9_20pp.csv")

from matplotlib import pyplot as plt 

fig, axes = plt.subplots()
axes.plot(power_dataframe['n_trials'], power_dataframe[power_A], "ro")
axes.set_ylim([0, 1.1])
axes.set_xlim([0, max(all_used_trials) + 10])
axes.set_title("Power plot: {} pp, power = P(corr(p_est, p) > {})".format(n_pp, cut_off))
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0)

fig.savefig(power_A + '.png')



"""

* met 50 pp: correlatie al vanaf 10 trials altijd boven de 80%, dus power = 100% 
* met 20 pp: power bij 10 trials is 93,18%; 99,13%; 98,8% voor cut-off = 0.8
* met 10 pp: power bij 10 trials is - 94,54% voor cut-off = 0.8
                                    - 57.32%, 57.11% voor cut-off = 0.9


Remark: als er teveel p = 0 of p = 1 zijn, dan zal dit de correlatie omhoog trekken, want dan 
is de p_estimate sowieso correct 
"""
