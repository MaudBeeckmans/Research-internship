# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 09:49:34 2021

@author: Maud
"""
import pandas as pd
import numpy as np
from Functions_EEG_experiment import softmax, rescorla_wagner
import os
from scipy import optimize


def likelihood_realdata(learning_rate_estimate, file_name, n_trials):
    """File_name: should contain path towards the file of this pp."""
    global data
    data = pd.read_table(file_name, sep = '\t')
    values = np.array([[0.5, 0.5], [0.5, 0.5]])
    actual_rewards = data['FB'][:n_trials]
    actual_choices = (data['Resp'][:n_trials] == 'j')*1
    stimuli = data['Grating'][:n_trials]
    logL = 0
    for trial in range(n_trials):
        stimulus = int(stimuli[trial])
        chosen_action = actual_choices[trial].astype(int)
        rew_this_trial = actual_rewards[trial]
        stimulus_weights = values[stimulus, :]
        probabilities = softmax(current_values = stimulus_weights, temperature = 0.41)
        current_likelihood = probabilities[chosen_action]
        
        logL = logL + np.log(current_likelihood)
        PE, updated_value = rescorla_wagner(previous_value = values[stimulus, chosen_action], 
                                                obtained_rew = rew_this_trial, 
                                                learning_rate = learning_rate_estimate) 
        values[stimulus, chosen_action] = updated_value
    return -logL

folder = os.path.join(os.getcwd(), 'Behavioral_Data')
n_pp = 34
participants = np.arange(1, n_pp*1, 1)
trials = np.array([100, 200, 300, 400, 480])

estimation_DF = pd.DataFrame(columns = trials.astype(str), 
                             index = participants)

for pp in participants: 
    print("We're at pp {}".format(pp))
    file_name = os.path.join(folder, 
                "Probabilistic_Reversal_task_subject_{}_Session_0_data.tsv".format(pp))
    Estimation_folder = os.path.join(os.getcwd(), 'Estimations_realpp')
    if not os.path.isdir(Estimation_folder):
        os.mkdir(Estimation_folder)
    Estimation_file = os.path.join(Estimation_folder, 'Estimate_realpp_fmin.csv')
    for n_trials in trials: 
        # estim_param2 = optimize.fmin(likelihood_realdata, np.random.rand(1), 
        #                                  args =(tuple([file_name, n_trials])), 
        #                                  maxfun= 100000, xtol = 0.001)
        estim_param = optimize.differential_evolution(likelihood_realdata, [(0,1)], 
                                                      args = (tuple([file_name, n_trials])), 
                                                  maxiter = 100000, tol = 0.005)
        estimation_DF[str(n_trials)][pp] = estim_param.x
estimation_DF.to_csv(Estimation_file)

    
    




