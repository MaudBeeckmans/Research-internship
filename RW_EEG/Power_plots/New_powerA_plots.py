# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 08:57:28 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat


"""First cell: save the power_estimates for all fixed Temperatures used for the 3 groups in 1 dataframe per used_temperature
    Cell 3: make 3D plot per group over all used_Temperatures """

#%% Cell1: preparations; load the correct learning rates (learning_rates) and estimations dataframe (input_df)
# all these elements are to ensure that the correct estimation file is loaded and the correct text is shown on the graphs 

groups = np.arange(1, 4, 1)
power_DF = pd.DataFrame(columns = ['Group1', 'Group2', 'Group3'])
temperatures = np.array([0.2, 0.41, 0.6, 1.0])

for used_temperature in temperatures: 
    for group in groups: 
        n_reps = 100
        used_simulations = 80
        used_temperature = 0.6
        
        # load the correct learning rates for this group 
        learning_rates = pd.read_csv(os.path.join(os.getcwd(), 'Final_simul_est_files', 
                                                  'learning_rates_group{}.csv'.format(group)))['LR'][:used_simulations]
        
        # load the correct estimations for each repetitions and each trials for this group 
        input_df_path = os.path.join(os.getcwd(), 'Final_simul_est_files', 'Estimations_summary')
        input_df = pd.read_csv(os.path.join(input_df_path, 
                                               'Estimates_group{}_{}rep_tempfixed@{}.csv'.format(group, n_reps, used_temperature))).iloc[:used_simulations*n_reps, :]
        # define the different number of trials used to do the parameter estimation
        trials = input_df.columns[4:] 
        
        
        # create an array that will contain the correlation between the estimated and the real LRs for each repetition (shape = n_reps x the different used trials)
        correlations = np.empty(shape = (n_reps, trials.shape[0]))
        N_simulations = int(np.max(input_df['simul'])+1)
        
        # Loop: estimate the correlation between the real and estimated LRs for each repetition (1 rep takes into account all pp.)
        for rep in range(n_reps): 
            print("We're at repetition {}".format(rep))
            used_df = input_df[input_df["rep"].isin([rep])] # only use the LR estimates for this particular repetition 
            col_count = 0 #keep track of which column of the correlation array has to be filled in 
            # Loop: compute the correlation at this repetition with each of the LRs estimated with the different number of trials 
            for trial in trials: 
                # select the correct LR_estimates 
                alpha_est = used_df[trial].to_numpy().astype(float)
                alpha_est = np.round(alpha_est, 3)
                
                #Power option A: compute the correlations 
                cor = np.round(np.corrcoef(learning_rates, alpha_est)[0, 1], 2)
                correlations[rep, col_count] = cor
                col_count += 1
        power_cut_off = 0.8
        power = np.mean((correlations > power_cut_off)*1, axis = 0) #take the average across each column
           #result will be one power-value per n_trials-value 
        power_DF['Group{}'.format(group)] = power 
    
    power_DF.to_csv(os.path.join(os.getcwd(), 'Final_power_plots', 'PowerA_tempfixed@{}.csv'.format(used_temperature)))


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

for group in groups: 
    G_array = np.array([])
    for temp in used_temperatures:
        G = pd.read_csv(os.path.join(path, 'PowerA_tempfixed@{}.csv'.format(temp)))['Group{}'.format(group)]
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
    fig.suptitle('P(corr(LR, LR_est) > 0.8) for group {}'.format(group), fontweight = 'bold')
    fig.savefig(os.path.join(os.getcwd(), 'Final_power_plots', 'PowerA_fixedtemps_group{}'.format(group)))







