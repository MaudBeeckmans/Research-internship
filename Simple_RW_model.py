# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:47:49 2021

@author: Maud
"""

"""Script: includes the creation of a simple Rescorla-Wagner model with the softmax rule
- there are 2 optiont to choose from on each trial: left or right response 
- option 1 has probability 0.2 of resulting in reward; option 2 probability 0.8"""

import pandas
import numpy as np


def softmax(current_values = np.array([0, 0]), temperature = 1): 
    probabilities = np.exp(current_values*temperature) / np.sum((np.exp(current_values[0]*temperature)+np.exp(current_values[1]*temperature)))
    # is the softmax function
    return probabilities

#function to choose option L with probability 'probabilityL'
    #returns 0 when optionL is not chosen, 1 when optionL is chosen 
def choose_option(prob = np.array([0.5, 0.5])): 
    choice = (np.random.random() <= prob[1])*1 
        #whether you choose the option that has probability prob or not 
        # 1 if you choose this option, 0 if you don't 
    return choice

def get_reward(prob = 0.5): 
    rew_present = (np.random.random() <= prob)*1
    return rew_present

def rescorla_wagner(previous_value = 0, obtained_rew = 0, learning_rate = 0.1): 
    PE = obtained_rew - previous_value
    value = previous_value + PE*learning_rate
    return PE, value 
    

alpha = 0.1
gamma = 1
rew_per_trial = 1 #how much you gain on a rewarded trial 
n_trials = 100
values = np.array([0.0, 0.0])
rew_probabilities = np.array([0.2, 0.8])

for trial in range(n_trials): 
    probabilities = softmax(current_values = values, temperature = gamma)
    #print("The chance of choosing each option is {}".format(probabilities))
    choice = choose_option(prob = probabilities)
    #print("Which option was chosen? {}".format(choice))
        # left = 0, right = 1 
    rew_present = get_reward(prob = rew_probabilities[choice])
    #print("Did our choice result in reward? {}".format(rew_present))
        # rew contains whether reward was obtained or not (obtained = 1, not obtained = 0)
        # if choose_R = 1, then take element 1 in the rew_probabilities (belongs to R resp)
        # if choose_R = 0, then take element 1 in the rew_probabilities (belongs to L resp)
    rew_this_trial = rew_present * rew_per_trial
    PE, updated_value = rescorla_wagner(previous_value = values[choice], 
                                        obtained_rew = rew_this_trial, learning_rate = alpha)
    # print(PE, updated_value)
    values[choice] = updated_value
    #print(values)
print(values)
    
    
    
    
    
    
    
    
    
