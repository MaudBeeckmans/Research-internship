# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 10:40:00 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from scipy import stats as stat

# all these elements are to ensure that the correct estimation file is loaded and the correct text is shown on the graphs 
n_reps = 100
reps = np.arange(0, n_reps, 1)
N_pp = 200
participants = np.arange(0, N_pp, 1)
used_N_pp = 20
selected_pp = np.random.choice(participants, size = used_N_pp, replace = False)
temp_type = 'variable' # should be 'variable' or 'fixedat0.2' e.g.
seed = '_seed23'
# seed = ''

trials = np.concatenate([np.array([50]), np.arange(100, 1500, 100), np.array([1440])])
# define the base folders for the INPUT files
param_folder =  os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', 'True_parameters_{}pp{}'.format(N_pp, seed))
base_LRfolder = os.path.join(os.environ.get('VSC_SCRATCH'), 'RW_EEG_final', 'Estimations_LR')

# define the base folders for the OUTPUT files (where the correlations will be stored)
power_folder = os.path.join(os.environ.get('VSC_DATA'), 'RW_EEG_final', 'Power', 'Power_Temp{}_{}pp{}_{}reps'.format(temp_type, 
                                                                                                             N_pp, seed, n_reps))
if not os.path.isdir(power_folder): os.makedirs(power_folder)


#%% Generate the correlations within each group (preparations for power A)
groups = np.array([1, 2, 3])

for group in groups: 
    # define where you'll store the correlations 
    correlation_file = os.path.join(power_folder, 'Correlations_group{}_{}ppused.csv'.format(group, used_N_pp))
    correlation_spearman_file = os.path.join(power_folder, 'Correlationsspearman_group{}_{}ppused.csv'.format(group, used_N_pp))
    
    if os.path.isfile(correlation_file) and os.path.isfile(correlation_spearman_file):
        print('Correlations for group {} already stored.'.format(group))
    else: 
        
        # define where you can find the estimated LRs for each group within each repetition 
        LREstimation_folder = os.path.join(base_LRfolder, 'LREstimations_group{}_Temp{}_{}pp{}'.format(group, 
                                                                                        temp_type, N_pp, seed))
        
        
        
        # create epmty array that will contain the correlations eventually 
        correlations = pd.DataFrame(columns = trials, index = np.arange(0, n_reps, 1))    
        correlations_spearman = pd.DataFrame(columns = trials, index = np.arange(0, n_reps, 1))    
        
        for rep_number in reps: 
            # Deduce the True LRs for this rep and this group 
            param_DF = pd.read_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep_number)))
            # define the true LRs (are the same over all n_trials used)
            True_LRs = np.array(param_DF['LR_g{}'.format(group)])
            True_LRs = True_LRs[selected_pp]
            
            # deduce the Estimated LRs for all n_trials in this rep and this group
            LREstimation_file = os.path.join(LREstimation_folder, 'LREstimate_rep{}.csv'.format(rep_number))
            LREstimation_DF = pd.read_csv(LREstimation_file)
        
            
            
            for n_trials in trials: 
                # define the current LR estimates for each pp within this repetition and this group
                Estimated_LRs = np.array(LREstimation_DF[str(n_trials)])
                Estimated_LRs = Estimated_LRs[selected_pp]
                # calculate the correlation between the True & estimated LRs 
                cor = np.round(np.corrcoef(True_LRs, Estimated_LRs)[0, 1], 2)
                cor_spearman, p_spearman = stat.spearmanr(True_LRs, Estimated_LRs)
                cor_spearman = np.round(cor_spearman, 3)
                # store the correlation for this repetition and this n_trials used for estimation of the LRs
                correlations.loc[rep_number, n_trials] = cor
                correlations_spearman.loc[rep_number, n_trials] = cor_spearman
        correlations.to_csv(correlation_file, index = False)
        correlations_spearman.to_csv(correlation_spearman_file, index = False)

#%% Correlations with bound on LR = 1
for group in groups: 
    correlation_bound1_file = os.path.join(power_folder, 'Correlationsbound1_group{}_{}ppused.csv'.format(group, used_N_pp))
    if os.path.isfile(correlation_bound1_file): print('Correlations_bound1 already stored for group {}.'. format(group))
    else: 
        # define where you can find the estimated LRs for each group within each repetition 
        LREstimation_folder = os.path.join(base_LRfolder, 'LREstimations_group{}_Temp{}_{}pp{}'.format(group, 
                                                                                        temp_type, N_pp, seed))
        
        # create epmty array that will contain the correlations eventually 
        correlations_bound1 = pd.DataFrame(columns = trials, index = np.arange(0, n_reps, 1))    
        
        for rep_number in reps: 
            # Deduce the True LRs for this rep and this group 
            param_DF = pd.read_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep_number)))
            # define the true LRs (are the same over all n_trials used)
            True_LRs = np.array(param_DF['LR_g{}'.format(group)])
            True_LRs = True_LRs[selected_pp]
            
            # deduce the Estimated LRs for all n_trials in this rep and this group
            LREstimation_file = os.path.join(LREstimation_folder, 'LREstimate_rep{}.csv'.format(rep_number))
            LREstimation_DF = pd.read_csv(LREstimation_file)
        
            
            
            for n_trials in trials: 
                # define the current LR estimates for each pp within this repetition and this group
                Estimated_LRs = np.array(LREstimation_DF[str(n_trials)])
                Estimated_LRs = Estimated_LRs[selected_pp]
                Estimated_LRs = np.where(Estimated_LRs > 1, 1, Estimated_LRs)
                # calculate the correlation between the True & estimated LRs 
                cor = np.round(np.corrcoef(True_LRs, Estimated_LRs)[0, 1], 2)
                # store the correlation for this repetition and this n_trials used for estimation of the LRs
                correlations_bound1.loc[rep_number, n_trials] = cor
        correlations_bound1.to_csv(correlation_bound1_file, index = False)
        



#%% Generate the t-statistics for each group comparison (store ES & P-values)

def cohen_d(x, y): 
    cohen_d = (np.mean(x) - np.mean(y)) /np. sqrt((np.std(x, ddof=1) ** 2 + np.std(y, ddof=1) ** 2) / 2.0)
    return cohen_d


compared_groups = np.array([[1, 2], [1, 3], [2, 3]])
for groups in compared_groups: 
    # define where you'll store the P_values & the ES
    PValue_file = os.path.join(power_folder, 'PValues_group{}_{}ppused.csv'.format(groups, used_N_pp))
    ES_file = os.path.join(power_folder, 'ES_group{}_{}ppused.csv'.format(groups, used_N_pp))
    
    if os.path.isfile(PValue_file) and os.path.isfile(ES_file): 
        print('P_values & ES already stored for these groups: {}.'.format(groups))
    else: 
        # define where you can find the estimated LRs for each group within each repetition 
        LREstimation_folderA = os.path.join(base_LRfolder, 'LREstimations_group{}_Temp{}_{}pp{}'.format(groups[0], 
                                                                                        temp_type, N_pp, seed))
        LREstimation_folderB = os.path.join(base_LRfolder, 'LREstimations_group{}_Temp{}_{}pp{}'.format(groups[1], 
                                                                                        temp_type, N_pp, seed))
        # create epmty DFs that will contain the P_values & ES eventually 
        PValues = pd.DataFrame(columns = np.concatenate([['True_P'], trials]), index = np.arange(0, n_reps, 1)) 
        ES = pd.DataFrame(columns = np.concatenate([['True_ES'], trials]), index = np.arange(0, n_reps, 1)) 
        
        
        for rep_number in reps: 
            # Deduce the True LRs for this rep and these groups 
            param_DF = pd.read_csv(os.path.join(param_folder, 'True_parameters_rep{}.csv'.format(rep_number)))
            # define the true LRs (are the same over all n_trials used)
            True_LRsA = np.array(param_DF['LR_g{}'.format(groups[0])])
            True_LRsB = np.array(param_DF['LR_g{}'.format(groups[1])])
            
            True_LRsA = True_LRsA[selected_pp]
            True_LRsB = True_LRsB[selected_pp]
            
            True_T, True_P = stat.ttest_ind(True_LRsA, True_LRsB)
            PValues.loc[rep_number, 'True_P'] = np.round(True_P, 5)
            True_ES = cohen_d(True_LRsB, True_LRsA)
            ES.loc[rep_number, 'True_ES'] = np.round(True_ES, 5)
            
            
            # deduce the Estimated LRs for all n_trials in this rep and these groups
            LREstimation_fileA = os.path.join(LREstimation_folderA, 'LREstimate_rep{}.csv'.format(rep_number))
            LREstimation_fileB = os.path.join(LREstimation_folderB, 'LREstimate_rep{}.csv'.format(rep_number))
            LREstimation_DFA = pd.read_csv(LREstimation_fileA)
            LREstimation_DFB = pd.read_csv(LREstimation_fileB)
            
            for n_trials in trials: 
                # define the current LR estimates for each pp within this repetition and this group
                Estimated_LRsA = np.array(LREstimation_DFA[str(n_trials)])
                Estimated_LRsB = np.array(LREstimation_DFB[str(n_trials)])
                
                Estimated_LRsA = Estimated_LRsA[selected_pp]
                Estimated_LRsB = Estimated_LRsB[selected_pp]
                
                # Calculate the T-statistic for the group comparison of LRs 
                Estim_T, Estim_P = stat.ttest_ind(Estimated_LRsA, Estimated_LRsB)
                # Store the P_value from the T-statistic
                PValues.loc[rep_number, str(n_trials)] = np.round(Estim_P, 5)
                # store the ES for this repetition, this n_trials and this group
                Estim_ES = cohen_d(Estimated_LRsB, Estimated_LRsA)
                ES.loc[rep_number, str(n_trials)] = np.round(Estim_ES, 5)
        
        # stre the arrays into csv-files
        PValues.to_csv(PValue_file, index = False)
        ES.to_csv(ES_file, index = False)
            
            
                
                
            
        







