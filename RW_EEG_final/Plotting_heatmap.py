# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 16:07:44 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
import seaborn as sns 

n_reps = 400
reps = np.arange(1, n_reps, 1)
# reps = np.delete(reps, np.array([1, 5, 7, 8, 11, 12, 14, 16, 21, 31, 32]))
N_pp = 200
used_pp_array = np.array([200, 100, 50, 20])
temp_type = 'variable' # should be 'variable' or 'fixedat0.2' e.g.
seed = '_seed23'
# seed = ''
# define the base folders for the INPUT files
power_folder = os.path.join(os.getcwd(), 'Power', 'Power_Temp{}_{}pp{}_{}reps'.format(temp_type, N_pp, seed, n_reps))
plot_folder = os.path.join(power_folder, 'Power_plots')
if not os.path.isdir(plot_folder): os.mkdir(plot_folder)

trials = np.concatenate([np.array([50]), np.arange(100, 1500, 100), np.array([1440])])

#%% Power A plots heatmap 
powerA_cut_off = 0.7
powerA_text = 'Power = P(corr(p_est, p) > {}) with {} reps'.format(powerA_cut_off, n_reps)

groups = np.array([1, 2, 3])

for group in groups: 
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    
    i = 0
    for used_pp in used_pp_array: 
        pp_used = '_{}ppused'.format(used_pp)
    
        # define where you can find the stored correlations 
        correlation_file = os.path.join(power_folder, 'Correlations_group{}{}.csv'.format(group, pp_used))
        correlations = pd.read_csv(correlation_file)
        
        powerA = (correlations >= powerA_cut_off)*1
        powerA = np.array(powerA)[reps, :]
        powerA_proportions = np.mean(np.array(powerA), 0)
        if i == 0: powerA_proportions_pp = powerA_proportions
        else: powerA_proportions_pp = np.row_stack([powerA_proportions_pp, powerA_proportions])
        i += 1
    
    
    sns.heatmap(powerA_proportions_pp, vmin = 0, vmax = 1, ax = axes, cmap = "viridis")
    fig.suptitle(powerA_text, fontweight = 'bold')
    plt.yticks(np.arange(0, 4, 1), used_pp_array)
    plt.xticks(np.arange(0, trials.shape[0], 3), trials[np.arange(0, trials.shape[0], 3)])
    axes.set_ylabel('participants', loc = 'top')
    axes.set_xlabel('trials', loc = 'right')
    axes.set_title('Group {}'.format(group))
    
    fig.savefig(os.path.join(plot_folder, 'heatmap_powerA_group{}_{}.png'.format(group, powerA_cut_off)))

#%%Correlations plot heatmap 



groups = np.array([1, 2, 3])

for group in groups: 
    fig, axes = plt.subplots(nrows = 1, ncols = 1, sharex = True, sharey = True)
    i = 0
    for used_pp in used_pp_array: 
        pp_used = '_{}ppused'.format(used_pp)
        # define where you can find the stored correlations 
        correlation_file = os.path.join(power_folder, 'Correlations_group{}{}.csv'.format(group, pp_used))
        correlations = pd.read_csv(correlation_file)
        correlations = np.array(correlations)[reps, :]
        mean_correlation = np.mean(correlations, axis = 0)
        if i == 0: mean_correlations_pp = mean_correlation
        else: mean_correlations_pp = np.row_stack([mean_correlations_pp, mean_correlation])
        i += 1
    sns.heatmap(mean_correlations_pp, vmin = 0, vmax = 1, ax = axes, cmap = "viridis")
    fig.suptitle('Correlations with {} reps'.format(n_reps), fontweight = 'bold')
    plt.yticks(np.arange(0, 4, 1), used_pp_array)
    plt.xticks(np.arange(0, trials.shape[0], 3), trials[np.arange(0, trials.shape[0], 3)])
    axes.set_ylabel('participants', loc = 'top')
    axes.set_xlabel('trials', loc = 'right')  
    axes.set_title('Group {}'.format(group))      
    fig.savefig(os.path.join(plot_folder, 'heatmap_correlations_group{}.png'.format(group)))

#%%Correlations spearman plot heatmap 

groups = np.array([1, 2, 3])

for group in groups: 
    fig, axes = plt.subplots(nrows = 1, ncols = 1, sharex = True, sharey = True)
    i = 0
    for used_pp in used_pp_array: 
        pp_used = '_{}ppused'.format(used_pp)
        # define where you can find the stored correlations 
        correlation_file = os.path.join(power_folder, 'Correlationsspearman_group{}{}.csv'.format(group, pp_used))
        correlations = pd.read_csv(correlation_file)
        correlations = np.array(correlations)[reps, :]
        mean_correlation = np.mean(correlations, axis = 0)
        if i == 0: mean_correlations_pp = mean_correlation
        else: mean_correlations_pp = np.row_stack([mean_correlations_pp, mean_correlation])
        i += 1
    sns.heatmap(mean_correlations_pp, vmin = 0, vmax = 1, ax = axes, cmap = "viridis")
    fig.suptitle('Spearman correlations with {} reps'.format(n_reps), fontweight = 'bold')
    plt.yticks(np.arange(0, 4, 1), used_pp_array)
    plt.xticks(np.arange(0, trials.shape[0], 3), trials[np.arange(0, trials.shape[0], 3)])
    axes.set_ylabel('participants', loc = 'top')
    axes.set_xlabel('trials', loc = 'right')  
    axes.set_title('Group {}'.format(group))      
    fig.savefig(os.path.join(plot_folder, 'heatmap_correlationsspearman_group{}.png'.format(group)))
    



#%% Power B heatmaps 
compared_groups = np.array([[1, 2], [1, 3], [2, 3]])
powerB_cut_off = 0.05 # *2 since t-test we used was 2-sided, but we want 1-sided t-test?
powerB_text = 'Power = P(Ga < Gb) with p-value < {} with {} reps'.format(powerB_cut_off, n_reps)



for groups in compared_groups: 
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    i = 0
    for used_pp in used_pp_array: 
        pp_used = '_{}ppused'.format(used_pp)
        # define where you can find the stored P_values & ES
        PValue_file = os.path.join(power_folder, 'PValues_group{}{}.csv'.format(groups, pp_used))        
        PValues = pd.read_csv(PValue_file)
        
        powerB = (PValues <= powerB_cut_off*2)*1
        powerB = np.array(powerB)[reps, 1:]
        powerB_proportions = np.mean(powerB, axis = 0)
        
        if i == 0: powerB_proportions_pp = powerB_proportions
        else: powerB_proportions_pp = np.row_stack([powerB_proportions_pp, powerB_proportions])
        i += 1
        
    
    sns.heatmap(powerB_proportions_pp, vmin = 0, vmax = 1, ax = axes, cmap = "viridis")
    fig.suptitle(powerB_text, fontweight = 'bold')
    plt.yticks(np.arange(0, 4, 1), used_pp_array)
    plt.xticks(np.arange(0, trials.shape[0], 3), trials[np.arange(0, trials.shape[0], 3)])
    axes.set_ylabel('participants', loc = 'top')
    axes.set_xlabel('trials', loc = 'right')
    axes.set_title('Group {} vs. group {}'.format(groups[0], groups[1]))
    
    fig.savefig(os.path.join(plot_folder, 'heatmap_powerB_group{}_{}.png'.format(groups, powerB_cut_off)))
    







