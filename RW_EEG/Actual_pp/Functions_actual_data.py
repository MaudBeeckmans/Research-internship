# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 13:16:44 2021

@author: Maud
"""

import pandas as pd
import numpy as np
from Functions_EEG_experiment import softmax, rescorla_wagner
import os
from scipy import optimize


def likelihood_realdata(params, file_name, n_trials):
    # print(params)
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
        probabilities = softmax(current_values = stimulus_weights, temperature = params[1])
        current_likelihood = probabilities[chosen_action]
        
        logL = logL + np.log(current_likelihood)
        PE, updated_value = rescorla_wagner(previous_value = values[stimulus, chosen_action], 
                                                obtained_rew = rew_this_trial, 
                                                learning_rate = params[0]) 
        values[stimulus, chosen_action] = updated_value
    return -logL

def Value_PE_estimation(params, file_name, n_trials):
    Value_series = np.array([])
    PE_series = np.array([])
    data = pd.read_table(file_name, sep = '\t')
    values = np.array([[0.5, 0.5], [0.5, 0.5]])
    actual_rewards = data['FB'][:n_trials]
    actual_choices = (data['Resp'][:n_trials] == 'j')*1
    stimuli = data['Grating'][:n_trials]
    for trial in range(n_trials):
        stimulus = int(stimuli[trial])
        chosen_action = actual_choices[trial].astype(int)
        rew_this_trial = actual_rewards[trial]
        stimulus_weights = values[stimulus, :]
        probabilities = softmax(current_values = stimulus_weights, temperature = params[1])
        PE, updated_value = rescorla_wagner(previous_value = values[stimulus, chosen_action], 
                                                obtained_rew = rew_this_trial, 
                                                learning_rate = params[0]) 
        Value_series = np.append(Value_series, values[stimulus, chosen_action])
        PE_series = np.append(PE_series, PE)
        values[stimulus, chosen_action] = updated_value
    return Value_series, PE_series, actual_rewards