# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:06:08 2021

@author: Maud
"""

import numpy as np
from General_RW_functions import softmax, choose_bandit, get_reward, rescorla_wagner
import pandas as pd 

def likelihood(learning_rate_estimate, file_name, n_trials):
    """Function to estimate the likelihood of a given parameter combination (learning_rate
    and temperature) given the data. Actual_choices, actual_rewards and start_values are
    drawn from the actual data of the participant. Returns the logL for these parameter values, 
    the higher the logL, the better! Thus if want to minimize, take -logL and find minimum!"""
    data = pd.read_csv(file_name)
    real_alpha = data['learning_rate'][0]
    # n_trials = data.shape[0]
    values = np.array([0.5, 0.5])
    actual_rewards = data['rewards'][:n_trials]
    actual_choices = data['choices'][:n_trials]
    temperature_estimate = data['temperature'][0]
    logL = 0
    for trial in range(n_trials): 
        #The choice that was made at this trial and whether reward was received
        choice = actual_choices[trial].astype(int)
        rew_this_trial = actual_rewards[trial]
        #calculate the probability of each choice at this trial given the Values
             #Values are updated with current_learning_rate
        probabilities = softmax(current_values = values, temp = temperature_estimate)
        current_likelihood = probabilities[choice]
        logL = logL + np.log(current_likelihood)
        # print(current_likelihood)
        PE, updated_value = rescorla_wagner(previous_value = values[choice], 
                                                obtained_rew = rew_this_trial, 
                                                alpha = learning_rate_estimate) 
        values[choice] = updated_value
    return -logL
        
