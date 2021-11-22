# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:57:08 2021

@author: Maud
"""
import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 


n_reps = 400
reps = np.arange(0, n_reps, 1)
# reps = np.delete(reps, np.array([0, 9, 13]))
N_pp = 200
temp_type = 'variable' # should be 'variable' or 'fixedat0.2' e.g.
seed = '_seed23'
# seed = ''
used_pp = 200
pp_used = '_{}ppused'.format(used_pp)

trials = np.concatenate([np.array([50]), np.arange(100, 1500, 100), np.array([1440])])
# define the base folders for the INPUT files
power_folder = os.path.join(os.getcwd(), 'Power', 'Power_Temp{}_{}pp{}_{}reps'.format(temp_type, N_pp, seed, n_reps))
plot_folder = os.path.join(power_folder, 'Power_plots')
if not os.path.isdir(plot_folder): os.mkdir(plot_folder)

colors = ['blue', 'orange', 'green']


#%% Power A plotting 

groups = np.array([1, 2, 3])
# groups = np.array([[1, 2], [2, 3], [1, 3]])
if seed == '_seed24': groups = np.array([0])
powerA_cut_off = 0.7
powerA_text = 'Power = P(corr(p_est, p) > {}) with {} reps'.format(powerA_cut_off, n_reps)


fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.set_ylim([-0.1, 1.1])
axes.set_xlim([0, int(trials[-1])])
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0)


i = 0
for group in groups: 
    # define where you can find the stored correlations 
    correlation_file = os.path.join(power_folder, 'Correlations_group{}{}.csv'.format(group, pp_used))
    correlations = pd.read_csv(correlation_file)
    powerA = (correlations >= powerA_cut_off)*1
    powerA = np.array(powerA)[reps, :]
    powerA_proportions = np.mean(np.array(powerA), 0)
    
    axes.plot(trials.astype(int), powerA_proportions, '--o', color = colors[i], label = 'Group {}'.format(group))
    i += 1

axes.set_title('{} pp per group, temperature {}'.format(used_pp, temp_type))
fig.suptitle(powerA_text, fontweight = 'bold')
axes.legend()
fig.tight_layout()
fig.savefig(os.path.join(plot_folder, 'powerA_{}ppused_{}.png'.format(used_pp, powerA_cut_off)))
#%% Plotting the correlation and the standard error of the correlation? 

fig, axes = plt.subplots(nrows = 1, ncols = 2, sharex = True, sharey = True)
axes[0].set_ylim([-0.1, 1.1])
axes[0].set_xlim([0, int(trials[-1])])
axes[0].set_xlabel('N_trials', loc = 'right')
axes[1].set_xlabel('N_trials', loc = 'right')
y_label = axes[0].set_ylabel('Correlation', loc = 'top')

i = 0
for group in groups: 
    # define where you can find the stored correlations 
    correlation_file = os.path.join(power_folder, 'Correlations_group{}{}.csv'.format(group, pp_used))
    correlations = pd.read_csv(correlation_file)
    correlationsB = np.array(correlations)[reps, :]
    mean_correlation = np.mean(correlations, axis = 0)
    stderror_correlation = np.std(correlations, axis = 0)/np.sqrt(correlations.shape[0])
    std_correlation = np.std(correlations, axis = 0)
    # print(mean_correlation)
    # print(stderror_correlation)
    axes[0].errorbar(x = trials.astype(int), y = mean_correlation, yerr = stderror_correlation, fmt = '--o', color = colors[i],
                  label = 'Group {}'.format(group))
    axes[1].errorbar(x = trials.astype(int), y = mean_correlation, yerr = std_correlation, fmt = '--o', color = colors[i],
                  label = 'Group {}'.format(group))
    i += 1
axes[0].set_title('Standard error')
axes[1].set_title('Standard deviation')
axes[0].plot([0,1500],[0.8,0.8], lw = 2, linestyle ="dashed", color ='k', label ='0.8')
axes[0].plot([0,1500],[0.9,0.9], lw = 2, linestyle ="dashed", color ='k', label ='0.9')
axes[0].plot([0,1500],[1,1], lw = 2, linestyle ="dashed", color ='k', label ='1.0')
fig.suptitle('Correlations with {} reps'.format(n_reps) + '\n{} pp per group, temperature {}'.format(used_pp, temp_type),
             fontweight = 'bold')
axes[1].legend()
fig.tight_layout()

fig.savefig(os.path.join(plot_folder, 'Correlations_{}ppused.png'.format(used_pp)))

#%% Plotting the correlation with bound1
# fig, axes = plt.subplots(nrows = 1, ncols = 2, sharex = True, sharey = True)
# axes[0].set_ylim([-0.1, 1.1])
# axes[0].set_xlim([0, int(trials[-1])])
# axes[0].set_xlabel('N_trials', loc = 'right')
# axes[1].set_xlabel('N_trials', loc = 'right')
# y_label = axes[0].set_ylabel('Correlation bound 1', loc = 'top')

# i = 0
# for group in groups: 
#     # define where you can find the stored correlations 
#     correlation_file = os.path.join(power_folder, 'Correlationsbound1_group{}{}.csv'.format(group, pp_used))
#     correlations = pd.read_csv(correlation_file)
#     correlations = np.array(correlations)[reps, :]
#     mean_correlation = np.mean(correlations, axis = 0)
#     stderror_correlation = np.std(correlations, axis = 0)/np.sqrt(correlations.shape[0])
#     std_correlation = np.std(correlations, axis = 0)
#     # print(mean_correlation)
#     # print(stderror_correlation)
#     axes[0].errorbar(x = trials.astype(int), y = mean_correlation, yerr = stderror_correlation, fmt = '--o', color = colors[i],
#                   label = 'Group {}'.format(group))
#     axes[1].errorbar(x = trials.astype(int), y = mean_correlation, yerr = std_correlation, fmt = '--o', color = colors[i],
#                   label = 'Group {}'.format(group))
#     i += 1
# axes[0].set_title('Standard error')
# axes[1].set_title('Standard deviation')
# axes[0].plot([0,1500],[0.8,0.8], lw = 2, linestyle ="dashed", color ='k', label ='0.8')
# axes[0].plot([0,1500],[0.9,0.9], lw = 2, linestyle ="dashed", color ='k', label ='0.9')
# axes[0].plot([0,1500],[1,1], lw = 2, linestyle ="dashed", color ='k', label ='1.0')
# fig.suptitle('Correlations bound 1 with {} reps'.format(n_reps) + '\n{} pp per group, temperature {}'.format(used_pp, temp_type),
#              fontweight = 'bold')
# axes[1].legend()
# fig.tight_layout()

# fig.savefig(os.path.join(plot_folder, 'Correlationsbound1_{}ppused.png'.format(used_pp)))

#%% Plotting the spearman correlations

fig, axes = plt.subplots(nrows = 1, ncols = 2, sharex = True, sharey = True)
axes[0].set_ylim([-0.1, 1.1])
axes[0].set_xlim([0, int(trials[-1])])
axes[0].set_xlabel('N_trials', loc = 'right')
axes[1].set_xlabel('N_trials', loc = 'right')
y_label = axes[0].set_ylabel('Correlation', loc = 'top')

i = 0
for group in groups: 
    # define where you can find the stored correlations 
    correlation_file = os.path.join(power_folder, 'Correlationsspearman_group{}{}.csv'.format(group, pp_used))
    correlations = pd.read_csv(correlation_file)
    correlations = np.array(correlations)[reps, :]
    mean_correlation = np.mean(correlations, axis = 0)
    stderror_correlation = np.std(correlations, axis = 0)/np.sqrt(correlations.shape[0])
    std_correlation = np.std(correlations, axis = 0)
    # print(mean_correlation)
    # print(stderror_correlation)
    axes[0].errorbar(x = trials.astype(int), y = mean_correlation, yerr = stderror_correlation, fmt = '--o', color = colors[i],
                  label = 'Group {}'.format(group))
    axes[1].errorbar(x = trials.astype(int), y = mean_correlation, yerr = std_correlation, fmt = '--o', color = colors[i],
                  label = 'Group {}'.format(group))
    i += 1
axes[0].set_title('Standard error')
axes[1].set_title('Standard deviation')
axes[0].plot([0,1500],[0.8,0.8], lw = 2, linestyle ="dashed", color ='k', label ='0.8')
axes[0].plot([0,1500],[0.9,0.9], lw = 2, linestyle ="dashed", color ='k', label ='0.9')
axes[0].plot([0,1500],[1,1], lw = 2, linestyle ="dashed", color ='k', label ='1.0')
fig.suptitle('Spearman correlations with {} reps'.format(n_reps) + '\n{} pp per group, temperature {}'.format(used_pp, temp_type),
              fontweight = 'bold')
axes[1].legend()
fig.tight_layout()

fig.savefig(os.path.join(plot_folder, 'Correlationsspearman_{}ppused.png'.format(used_pp)))
    


    
    
    
#%% Power B plotting 

compared_groups = np.array([[1, 2], [1, 3], [2, 3]])
powerB_cut_off = 0.001 # *2 since t-test we used was 2-sided, but we want 1-sided t-test?
powerB_text = 'Power = P(Ga < Gb) with p-value < {} with {} reps'.format(powerB_cut_off, n_reps)


fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.set_ylim([-0.1, 1.1])
axes.set_xlim([0, int(trials[-1])])
axes.set_xlabel('N_trials', loc = 'right')
y_label = axes.set_ylabel('P', loc = 'top')
y_label.set_rotation(0)

i = 0
for groups in compared_groups: 
    # define where you can find the stored P_values & ES
    PValue_file = os.path.join(power_folder, 'PValues_group{}{}.csv'.format(groups, pp_used))
    ES_file = os.path.join(power_folder, 'ES_group{}{}.csv'.format(groups, pp_used))
    
    PValues = pd.read_csv(PValue_file)
    # ES =  pd.read_csv(ES_file).iloc[:, 1:]
    
    powerB = (PValues <= powerB_cut_off*2)*1
    powerB = np.array(powerB)[reps, :]
    powerB_proportions = np.mean(powerB, axis = 0)
    
    axes.plot(trials.astype(int), powerB_proportions[1:], '--o', color = colors[i], label = 'Groups {}'.format(groups))
    axes.plot(700, powerB_proportions[0], '--v', color = colors[i], label = 'True power Groups {}'.format(groups))
    i += 1

axes.set_title('{} pp per group, temperature {}'.format(used_pp, temp_type))
fig.suptitle(powerB_text, fontweight = 'bold')
axes.legend()
fig.tight_layout()

fig.savefig(os.path.join(plot_folder, 'powerB_{}ppused.png'.format(used_pp)))

#%% Plotting the ES 

fig, axes = plt.subplots(nrows = 1, ncols = 2, sharex = True, sharey = True)
axes[0].set_ylim([-0.1, 2.2])
axes[0].set_xlim([0, int(trials[-1])])
axes[0].set_xlabel('N_trials', loc = 'right')
axes[1].set_xlabel('N_trials', loc = 'right')
y_label = axes[0].set_ylabel('ES', loc = 'top')
y_label.set_rotation(0)


SD_pooled = np.sqrt((0.1**2+0.1**2)/2)
True_ES = np.array([1, 2, 1])

colors = ['blue', 'orange', 'green']

i = 0
for groups in compared_groups: 
    
    
    ES_file = os.path.join(power_folder, 'ES_group{}{}.csv'.format(groups, pp_used))
    ES =  pd.read_csv(ES_file)
    ES = np.array(ES)[reps, :]
    mean_ES = np.mean(ES, axis = 0)
    stderror_ES = np.std(ES, axis = 0)/np.sqrt(ES.shape[0])
    std_ES = np.std(ES, axis = 0)
    print(stderror_ES)
    axes[0].errorbar(trials.astype(int), mean_ES[1:], yerr = stderror_ES[1:], fmt = '--o', color = colors[i], label = 'Groups {}'.format(groups))
    axes[1].errorbar(trials.astype(int), mean_ES[1:], yerr = std_ES[1:], fmt = '--o', color = colors[i], label = 'Groups {}'.format(groups))
    axes[0].errorbar(700, mean_ES[0], yerr = stderror_ES[0], fmt = '--v', color = colors[i], label = 'True_ES Groups {}'.format(groups))
    axes[1].errorbar(700, mean_ES[0], yerr = std_ES[0], fmt = '--v', color = colors[i], label = 'True_ES Groups {}'.format(groups))
    i += 1

axes[0].set_title('Standard error')
axes[1].set_title('Standard deviation')
fig.suptitle('ES with {} reps'.format(n_reps) + '\n{} pp per group, temperature {}'.format(used_pp, temp_type), fontweight = 'bold')
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc = 'lower right')
fig.tight_layout()

fig.savefig(os.path.join(plot_folder, 'ES_{}ppused.png'.format(used_pp)))


    
    
    

    