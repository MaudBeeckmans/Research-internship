# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:56:50 2021

@author: Maud
"""

import pandas as pd
import numpy as np
from General_RW_functions import softmax, choose_bandit, get_reward, rescorla_wagner


def generate_parameters(mean = 0.1, std = 0.05, n_pp = 1):
    """Function to generate the learning rate or the temperatures for multiple participants: 
        - parameters are randomly chosen from normal distribution with mean = mean & std = std
        - one unique parameter is generated for each participant"""
    parameters = np.round(np.random.normal(loc = mean, scale = std, size = n_pp), 3)
    while np.any(parameters >= 1) or np.any(parameters <= 0): 
        parameters = np.where(parameters >= 1, 
                            np.round(np.random.normal(loc = mean, scale = std, size = 1), 3), 
                            parameters)
        parameters = np.where(parameters <= 0, 
                              np.round(np.random.normal(loc = mean, scale = std, size = 1), 3), 
                              parameters)
    return parameters

def simulate_data(learning_rates = None, temperatures = None, rew_per_trial = 1, 
                  n_trials = 1000, 
                  rew_probabilities = np.array([0.2, 0.8])):
    """Function with the following parameters: 
        - learning_rates: should contain the learning rates for all pp
        - temperatures: should contain the temperatures for all pp
        - rew_per_trial: best to be 1 (otherwise normalization needed)
        - n_trials: number of trials per pp
        - start_values: the initial values
        - rew_probabilities: the probability for each bandit to deliver reward"""
    df = pd.DataFrame(columns = ['learning_rate', 'temperature', 
                                 'choices', 'rewards', 'Value_series', 'PE_series'])
    n_pp = learning_rates.shape[0]
    for pp in range(n_pp):
        start_values = np.array([0.5, 0.5])
        choices = np.array([])
        PE_series = np.array([])
        Value_series = np.array([])
        rewards = np.array([])
        values = start_values
        # print(start_values)
        for trial in range(n_trials): 
            probabilities = softmax(current_values = values, temp = temperatures[pp])
            #print("The chance of choosing each option is {}".format(probabilities))
            choice = choose_bandit(prob = probabilities)
            #print("Which option was chosen? {}".format(choice))
                # left = 0, right = 1   
            choices = np.append(choices, choice)
            rew_present = get_reward(prob = rew_probabilities[choice])
            #print("Did our choice result in reward? {}".format(rew_present))
                # rew contains whether reward was obtained or not (obtained = 1, not obtained = 0)
                # if choose_R = 1, then take element 1 in the rew_probabilities (belongs to bandit 1)
                # if choose_R = 0, then take element 0 in the rew_probabilities (belongs to bandit 0)
            rew_this_trial = rew_present * rew_per_trial
            PE, updated_value = rescorla_wagner(previous_value = values[choice], 
                                                obtained_rew = rew_this_trial, 
                                                alpha = learning_rates[pp])
            PE_series = np.append(PE_series, PE)
            Value_series = np.append(Value_series, values[choice])
            rewards = np.append(rewards, rew_present)
            # print(PE, updated_value)
            values[choice] = updated_value
        df = df.append({'learning_rate': learning_rates[pp], 'temperature': temperatures[pp], 
                        'choices': choices, 'rewards': rewards, 'Value_series': Value_series,
                        'PE_series': PE_series}, 
                       ignore_index = True)
    return df 
    