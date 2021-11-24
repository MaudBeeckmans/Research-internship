# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 13:24:01 2021

@author: Maud
"""

import numpy as np
import pandas as pd 
import os
from scipy import optimize
from scipy import stats as stat
from Functions_EEG_experiment import softmax, choose_option, get_reward, rescorla_wagner, generate_parameters, simulate_RW, likelihood




def power_analysis_RW(required_power = 0.8, power_type = 'correlation', criterion_cutoff = 0.8):
    """required_power: the power you want
    power_type: function works for 'correlation' or 'group difference'
    criterion_cutoff: the correlation you'd require for the parameter correlation criterion or the p-value you'd require
    for the group difference criterion"""
    n_reps = 100
    n_reps = 3
    Temp_mean = [1] # Temp distribution always the same for 1 or 2 groups 
    Temp_sd = [0.5]
    LR_mean = [0.6, 0.7] # Mean LR differs between the 2 groups (with correlation only first is used, 
                         # with group differnce both groups are used)
    LR_sd = [0.1]
    N_pp = 200 # maximal amount of participants
    N_pp = 4
    participants = np.arange(0, N_pp, 1)
    # trials: different number of trials that will be used to do the parameter estimation 
    trials = np.concatenate([np.array([50]), np.arange(100, 1500, 100), np.array([1440])])
    trials = np.array([500])
    # used_pp_array: different number of participants that will be used to calculate the correlations/group-difference
    # used_pp_array = np.array([200, 100, 50, 20])
    used_pp_array = np.array([4, 2])
    
    # Create the array (power_basis) that will contain the correlations or the p-values depending on your power_type
    power_basis = np.empty([n_reps, used_pp_array.shape[0], trials.shape[0]])
    
    # loop over the n repetitions: within 1 rep do participant generation, data simulation, parameter estimation and 
        # correlation/t-test 
    for rep in range(n_reps): 
        print("we're at repetition {}".format(rep))
        if power_type == 'correlation': groups = np.array([0])
        else: groups = np.array([0, 1])
        True_parameters_DF = pd.DataFrame()
        
        # Create arrays that will contain all the estimated LRs and Temps with varying n_trials
        global LREstimation_DF, TempEstimation_DF
        TempEstimation_DF = pd.DataFrame(index = np.arange(0, N_pp))
        LREstimation_DF = pd.DataFrame(index = np.arange(0, N_pp))
        
        
        # loop over the groups (in the case of correlation there is only 1 group, with group difference there are 2)
        for group in groups: # This loop will contain the parameter generation, data simulation & parameter estimation
            #PARAMETER GENERATION#
            # Generate the true parameters for 200 participants (is the max. amount of pp. used)
                # Generate learning rates, inverse_temperatures & design used (10 different design options)
            True_parameters_DF['LR_g{}'.format(group)] = generate_parameters(mean = LR_mean[group], std = LR_sd[0], 
                                                                             n_pp = N_pp)
            True_parameters_DF['T_g{}'.format(group)] = generate_parameters(mean = Temp_mean[0], std = Temp_sd[0], 
                                                                            n_pp = N_pp)
            True_parameters_DF['Design_g{}'.format(group)]= np.random.randint(0, 10, size = N_pp)
            
            #DATA SIMULATION#
            # Fill in the true parameters 
            TempEstimation_DF['Real_Temp_g{}'.format(group)] = True_parameters_DF['T_g{}'.format(group)]
            
            # fill in the true parameters
            LREstimation_DF['Real_LR_g{}'.format(group)] = True_parameters_DF['LR_g{}'.format(group)]
            
            for pp in participants: 
                which_design = True_parameters_DF.loc[pp, 'Design_g{}'.format(group)]
                LR = LREstimation_DF.loc[pp, 'Real_LR_g{}'.format(group)]
                Temp = TempEstimation_DF.loc[pp, 'Real_Temp_g{}'.format(group)]
                # select the design for this participant 
                design_filename = 'Data{}.csv'.format(which_design)
                # Design_file = os.path.join(os.environ.get('VSC_HOME'), 'RW_EEG', 'Design', design_filename)
                Design_file = os.path.join(r'C:\Users\Maud\Documents\Psychologie\2e master psychologie\Research Internship\Start to model RI\Maud_Sims\RW\Data_to_fit', 
                                           design_filename)
                
                # generate the responses for this participant 
                total_reward, responses = simulate_RW(learning_rate = LR, design_file = Design_file, inverse_temperature = Temp, 
                                                      triple_trials = True)
                
                print("parameter_estimation started for pp {}".format(pp))
            
                #Parameter estimation#
                # code below is not efficient yet, since design file will be loaded twice as it is loaded above in the 
                    # function simulate_RW as well 
                start_design = pd.read_csv(Design_file)
                # start design is repeated 3x to generate 1440 trials instead of 480 trials
                start_design = start_design.append(start_design).append(start_design)
                start_design['Response'] = responses
                for n_trials in trials: #trials: contains how many trials will be used to estimate the parameter(s)
                    # n_trials defines how many trials are used to estimate the parameter(s) 
                    estim_param = optimize.fmin(likelihood, np.random.rand(2), args =(tuple([start_design, n_trials])), 
                                        maxfun= 1000, xtol = 0.001)
                    LR_estim = estim_param[0]
        
                    estimation_repeat = 0
                    while LR_estim < 0.01 and estimation_repeat < 5:
                        print('\nRepetition of estimation was !! for pp {} from rep {} with {} n_trials.'.format(pp, 
                                                                                rep, n_trials))
                        
                        estim_param = optimize.fmin(likelihood, np.random.rand(2), args =(tuple([start_design, n_trials])), 
                                    maxfun= 1000, xtol = 0.001)
                        LR_estim = estim_param[0]
                        estimation_repeat += 1
                    if LR_estim < 0.01 or LR_estim > 2: 
                        print('Warning, LR parameter has weird estimation: {}'.format(estim_param[0]))
                    
                    # store the best fitting parameter(s) in the estimation_DFs in the correct column (n_trials) and 
                        # correct row (this_rep)
                    LREstimation_DF.loc[pp, str(n_trials) + '_g{}'.format(group)] = np.round(estim_param[0], 3)
                    TempEstimation_DF.loc[pp, str(n_trials) + '_g{}'.format(group)] = np.round(estim_param[1], 3)
        
        #CALCULATE THE CURRENT POWER BASIS#   (correlation or t-test for this repetition)
        usedpp_count = 0
        for used_pp in used_pp_array: 
            selected_pp = np.random.choice(participants, size = used_pp, replace = False)
            if power_type == 'correlation': 
                True_LRs = np.array(LREstimation_DF['Real_LR_g0'])[selected_pp]
                trial_count = 0
                for n_trials in trials: 
                    Estimated_LRs = np.array(LREstimation_DF[str(n_trials) + '_g0'])[selected_pp]
                    cor = np.round(np.corrcoef(True_LRs, Estimated_LRs)[0, 1], 2)
                    power_basis[rep, usedpp_count, trial_count] = cor
                    trial_count += 1
            else: 
                trial_count = 0
                for trial in trials: 
                    Estimated_LRs_g0 = np.array(LREstimation_DF[str(n_trials) + '_g0'])[selected_pp]
                    Estimated_LRs_g1 = np.array(LREstimation_DF[str(n_trials) + '_g1'])[selected_pp]
                    # Calculate the T-statistic for the group comparison of LRs 
                    Estim_T, Estim_P = stat.ttest_ind(Estimated_LRs_g0, Estimated_LRs_g1)
                    power_basis[rep, usedpp_count, trial_count] = np.round(Estim_P, 5)
                    trial_count += 1
            usedpp_count += 1
    #CALCULATE THE POWER ITSELF#
    if power_type == 'correlation': criterion_reached = (power_basis >= criterion_cutoff)*1
    else: criterion_reached = (power_basis <= criterion_cutoff)*1
    power = np.mean(criterion_reached, axis = 0)
    power_df = pd.DataFrame(power, columns = trials, index = used_pp_array)
    
    return power_basis, power, power_df

# power_basis, power, power_df = power_analysis_RW(required_power = 0.8, power_type = 'correlation', criterion_cutoff = 0.8)
power_basis, power, power_df = power_analysis_RW(required_power = 0.8, power_type = 'group difference', criterion_cutoff = 0.001)
power_file = os.path.join(os.getcwd(), 'try1.csv')

from matplotlib import pyplot as plt
import seaborn as sns 

fig, axes = plt.subplots(nrows = 1, ncols = 1, sharex = True, sharey = True)
sns.heatmap(power, vmin = 0, vmax = 1, ax = axes, cmap = "viridis")
fig.suptitle('Power for your criterion', fontweight = 'bold')
# put a label for each number of pp used on the y-axis
plt.yticks(np.arange(0, power_df.index.shape[0], 1), power_df.index)
plt.xticks(np.arange(0, power_df.columns.shape[0], 1), power_df.columns[np.arange(0, power_df.columns.shape[0], 1)])
axes.set_ylabel('participants', loc = 'top')
axes.set_xlabel('trials', loc = 'right')  
        
        
        
        
        
        
        
        
        
