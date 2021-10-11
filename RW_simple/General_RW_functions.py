# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:45:13 2021

@author: Maud
"""

import pandas
import numpy as np


def softmax(current_values = np.array([0, 0]), temp = 1): 
    probabilities = np.exp(current_values*temp) / (np.exp(current_values[0]*temp)+np.exp(current_values[1]*temp))
    # is the softmax function
    return probabilities

#function to choose option L with probability 'probabilityL'
    #returns 0 when optionL is not chosen, 1 when optionL is chosen 
def choose_bandit(prob = np.array([0.5, 0.5])): 
    choice = (np.random.random() <= prob[1])*1 
        #whether you choose the option that has probability prob or not 
        # 1 if you choose this option, 0 if you don't 
    return choice

def get_reward(prob = 0.5): 
    rew_present = (np.random.random() <= prob)*1
    return rew_present

def rescorla_wagner(previous_value = 0, obtained_rew = 0, alpha = 0.1): 
    PE = obtained_rew - previous_value
    value = previous_value + PE*alpha
    return PE, value 



