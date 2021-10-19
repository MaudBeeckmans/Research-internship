# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 14:13:52 2021

@author: Maud
"""


import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat

#%%Cell 1: preparations; load the relevant estimation_files and learning_rate_files

n_reps = 100
pp_per_group = 80
used_groups = [1, 2]

learning_rates_g1 = pd.read_csv(os.path.join('Final_simul_est_files', 
                                             'pp_overview80_group{}.csv'.format(used_groups[0])))['LR'][:pp_per_group]
learning_rates_g2 = pd.read_csv(os.path.join('Final_simul_est_files', 
                                             'pp_overview80_group{}.csv'.format(used_groups[1])))['LR'][:pp_per_group]

#mean actual learning rate for each group
mean_LR_g1 = np.mean(learning_rates_g1)
mean_LR_g2 = np.mean(learning_rates_g2)
#standard deviation of the learning rates in each group 
std_g1 = np.std(learning_rates_g1)
std_g2 = np.std(learning_rates_g2)  
diff_LR = np.round(np.abs(mean_LR_g1-mean_LR_g2), 2) #difference in meanLR between the 2 groups 
pooled_std = np.round(np.sqrt(std_g1**2 + std_g2**2), 3) # the pooled standard deviation

#input_df_g?: contains the estimations for all trials and all repetitions for one group
    # columns = mostly the number of trials used to estimate the learning rate 
    # rows: for each participant there are n_reps rows (n_reps = number of repetitions)
input_df_path = os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary')

input_df_g1 = pd.read_csv(os.path.join(input_df_path, 
                                       'Estimates_group{}_{}rep.csv'.format(used_groups[0], n_reps))).iloc[:pp_per_group*n_reps, :]
input_df_g2 = pd.read_csv(os.path.join(input_df_path, 
                                       'Estimates_group{}_{}rep.csv'.format(used_groups[1], n_reps))).iloc[:pp_per_group*n_reps, :]

trials = input_df_g1.columns[4:] #column 1-3 are not important, other columns contain the number of trials used to estimate the LR 



# deduce the number of repetitions and number of simulations (pp) from one of the dataframes containing all the LR_estimates 
n_reps = int(np.max(input_df_g1['rep'])+1)
N_simulations = int(np.max(input_df_g1['simul'])+1)

#Compute the t-statistic and p-value for the real learning rates 
    #if this p-value > 0.05, there is no actual difference between 2 groups, thus no difference should be found with estimated LRs either
T_stat_real, P_value_real = stat.ttest_ind(learning_rates_g1, learning_rates_g2)
print('Real T-stat is {}, p is {}'.format(np.round(T_stat_real, 3), P_value_real))
#%% Cell2: Estimate the power for each possible number of trials (Power: P(group2 > group 1))

#Create empty array that will contain the P_value for each repetition (= rows) and each amount of trials used for the estimation (= ncols)
P_values = np.empty(shape = (n_reps, trials.shape[0]))

# Loop: calculate the statistical significance of the differnece between the 2 groups for each repetition 
    #store the p-values in one big array 'P_values'
for rep in range(n_reps): 
    # used_df_g?: defines which repetition we're currently looking at. For each repetition, P_value will be estimated for each n_trials
        #this dataframe contains all the LR_estimates for 1 repetition: thus N_simulations x all_n_trials
    used_df_g1 = input_df_g1[input_df_g1["rep"].isin([rep])]
    used_df_g2 = input_df_g2[input_df_g2["rep"].isin([rep])]
    col_count = 0 #keep track of which column of the P_values array has to be filled in 
    
    #Loop: for this repetition, compute the T-stat and P-value with the current number of trials used to estimate the LR 
    for trial in trials: 

        LR_est_g1 = used_df_g1[trial].to_numpy().astype(float)
        LR_est_g2 = used_df_g2[trial].to_numpy().astype(float)
        
        T_stat, P_value = stat.ttest_ind(LR_est_g1, LR_est_g2)

        P_values[rep, col_count] = P_value
        col_count += 1

power_cut_off = 0.001 #actual cut-off is 0.001; for the t-test this is multiplied by 2 since the function below uses a 2-sided t-test
                        # and we want a one-sided t-test
power = np.mean((P_values < power_cut_off*2)*1, axis = 0) #take the average across each column
   #result will be one power-value per n_trials-value

#%% Cell 3: Plot the power

fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.set_ylim([-0.1, 1.1]) #the possible power-values
axes.set_xlim([0, int(trials[-1])]) #the number of trials used to do the LR_estimation
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0) 
axes.plot(trials.astype(int), power, 'ro')  #plot the trials on x-axis and the power on y-axis
axes.set_title("{} pp/group, LR_difference = {}, pooled_std = {} \nP(LR_group1 > LR_group2) p_value < {} with {} reps"
               .format(N_simulations, diff_LR, pooled_std, power_cut_off, n_reps))




