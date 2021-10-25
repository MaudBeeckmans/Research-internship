# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:08:05 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat

"""First cell: save the power_estimates for all fixed Temperatures used for the 3 group_combinations in 1 dataframe per used_temperature
    Cell 3: make 3D plot per group_combination over all used_Temperatures """

#%%Cell 1: preparations; load the relevant estimation_files and learning_rate_files

group_options = np.array([[1,2], [1,3], [3,2]])
temperatures = np.array([0.2, 0.41, 0.6, 1.0])
power_DF = pd.DataFrame(columns = ['Group1&2', 'Group1&3', 'Group3&2'])


for used_temperature in temperatures: 
    for used_groups in group_options: 
        if np.any(used_groups == 3) and used_temperature == 0.41: n_reps = 1000
        else: n_reps = 100
        pp_per_group = 80
        power_cut_off = 0.001 #actual cut-off is 0.001; 
        
        learning_rates_g1 = pd.read_csv(os.path.join('Final_simul_est_files', 
                                                     'pp_overview80_group{}.csv'.format(used_groups[0])))['LR'][:pp_per_group]
        learning_rates_g2 = pd.read_csv(os.path.join('Final_simul_est_files', 
                                                     'pp_overview80_group{}.csv'.format(used_groups[1])))['LR'][:pp_per_group]
        
        #input_df_g?: contains the estimations for all trials and all repetitions for one group
            # columns = mostly the number of trials used to estimate the learning rate 
            # rows: for each participant there are n_reps rows (n_reps = number of repetitions)
        input_df_path = os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary')
        
        input_df_g1 = pd.read_csv(os.path.join(input_df_path, 
                                               'Estimates_group{}_{}rep_tempfixed@{}.csv'.format(used_groups[0], n_reps, used_temperature))).iloc[:pp_per_group*n_reps, :]
        input_df_g2 = pd.read_csv(os.path.join(input_df_path, 
                                               'Estimates_group{}_{}rep_tempfixed@{}.csv'.format(used_groups[1], n_reps, used_temperature))).iloc[:pp_per_group*n_reps, :]
        
        trials = input_df_g1.columns[4:] #column 1-3 are not important, other columns contain the number of trials used to estimate the LR 
    
        #Compute the t-statistic and p-value for the real learning rates 
            #if this p-value > 0.05, there is no actual difference between 2 groups, thus no difference should be found with estimated LRs either
        T_stat_real, P_value_real = stat.ttest_ind(learning_rates_g1, learning_rates_g2)
        print('Real T-stat is {}, p is {}'.format(np.round(T_stat_real, 3), P_value_real))
        
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


        # for the t-test the power cut-off is multiplied by 2 since the function below uses a 2-sided t-test and we want a one-sided t-test
        power = np.mean((P_values < power_cut_off*2)*1, axis = 0) #take the average across each column
        power_DF['Group{}&{}'.format(used_groups[0], used_groups[1])] = power 

    power_DF.to_csv(os.path.join(os.getcwd(), 'Final_power_plots', 'PowerB_tempfixed@{}.csv'.format(used_temperature)))

#%%


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import pandas as pd 
import os


path = os.path.join(os.getcwd(), 'Final_power_plots')

used_temperatures = np.array([0.2, 0.41, 0.6, 1])

for group in group_options: 
    G_array = np.array([])
    for temp in used_temperatures:
        G = pd.read_csv(os.path.join(path, 'PowerB_tempfixed@{}.csv'.format(temp)))['Group{}&{}'.format(group[0], group[1])]
        if temp == used_temperatures[0]:G_array = G
        else: G_array = np.row_stack([G_array, G])
        
    
    # fig = plt.figure()
    fig, ax = plt.subplots()
    # ax = fig.gca(projection='3d')
    X = np.array([50, 100, 200, 300, 480, 480*2, 480*3])
    for i in range(used_temperatures.shape[0]): 
        Y = G_array[i, :]
        Z = used_temperatures[i]
        
        # surf = ax.plot(X, Y, Z, zdir = 'y', label = 'T = {}'.format(Z))
        ax.plot(X, Y, label = 'T = {}'.format(Z))
    ax.set_xlabel('N_trials')
    # ax.set_zlabel('P', rotation = 0)
    # ax.set_ylabel('Temperature')
    ax.set_ylabel('P', rotation = 0)
    
    ax.legend()
    fig.suptitle('P(G{} > G{})with p-value < 0.001)'.format(group[0], group[1]), fontweight = 'bold')
    fig.savefig(os.path.join(os.getcwd(), 'Final_power_plots', 'PowerB_fixedtemps_group{}'.format(group)))
