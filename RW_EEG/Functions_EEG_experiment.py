# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:09:53 2021

@author: Maud
"""


import numpy as np
import pandas as pd 
import os

#%% General RW functions

def softmax(current_values = np.array([0, 0]), temperature = 1): 
    probabilities = np.exp(current_values/temperature) / np.sum((np.exp(current_values[0]/temperature)+np.exp(current_values[1]/temperature)))
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

def rescorla_wagner(previous_value = 0.0, obtained_rew = 1.0, learning_rate = 0.1): 
    PE = obtained_rew - previous_value
    value = np.sum([previous_value, np.multiply(PE, learning_rate)])
    return PE, value 

#%% Function to generate parameters from normal distribution with certain mean and std 
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


#%% Function to simulate data for one participant with a specific learning_rate, design_file and output_file 
def simulate_RW(learning_rate = 0.5, temperature = 0.41, design_file = None, triple_trials = False): 
    """Parameters within function 
        - learning rate: should be defined for this participant
        - temperature: is fixed at 0.2
        - design_file: should contain both the file name and the path towards the file 
        - data_file: should contain both the file name and the path towards the file"""
    responses = np.array([])

    design_DF = pd.read_csv(design_file)
    if triple_trials == True: design_DF = design_DF.append(design_DF).append(design_DF)
    
    n_trials = design_DF.shape[0]
    alpha = learning_rate
    gamma = temperature
    rew_per_trial = 10 #how much you gain on a rewarded trial 
    #important: values zijn voor de rules! Welke rule wil pp. uitvoeren 
    n_actions = 2
    n_stim = 2
    #values = np.random.uniform(size = (n_stim, n_actions))
    values = np.array([[0.5, 0.5], [0.5, 0.5]])
    total_reward = 0
    
    for trial in range(n_trials): 
        
        #define the variables you'll need for this trial (take them from the design_array)
        rule = design_DF.iloc[trial, 1]
        stimulus = np.int(design_DF.iloc[trial, 2])
        CorResp =  np.int(design_DF.iloc[trial, 4])
        FBcon = design_DF.iloc[trial, 5]
        
        # if trial == 0 or rule != prev_rule:
        #     print("\n\nRule changed; current rule is {}".format(rule))
        
        #define which weights are of importance on this trial (depending on which stimulus was shown)
        stimulus_weights = values[stimulus, :]
        # compute probability of each action on this trial (using the weights for each action with the stimulus of this trial)
        action_probabilities = softmax(current_values = stimulus_weights, temperature = gamma)
        # define which action is chosen (based on the probabilities)
        chosen_action = choose_option(prob = action_probabilities)
        #define whether reward was received this trial or not
        rew_present = ((chosen_action == CorResp and FBcon == 1) or (chosen_action!= CorResp and FBcon == 0))*1
        rew_present = np.float(rew_present)
        rew_this_trial = rew_present * rew_per_trial
        
        #compute the PE and the updated value for this trial (and this stimulus-action pair)
            # to compute the PE & updated value, just work with whether reward was present or not (why?)
        PE, updated_value = rescorla_wagner(values[stimulus, chosen_action], rew_present, alpha)
        
        #store the relevant variables in the array
        #store the response given on this trial 
        responses = np.append(responses, chosen_action)
        
        #update the value of the stimulus-action that was relevant this trial 
        values[stimulus, chosen_action] = updated_value
        
        
        prev_rule = rule
        total_reward = total_reward + rew_this_trial
        #print("Action = {}, Stimulus = {}; Rew = {}; updated values are {}".format(chosen_action, stimulus, rew_present, values))
    return total_reward, responses


#%% Function to estimate the likelihood given the data and the current parameter 

def likelihood(learning_rate_estimate, data, n_trials, used_temperature):
    """Function to estimate the likelihood of a given parameter combination (learning_rate
    and temperature) given the data. Actual_choices, actual_rewards and start_values are
    drawn from the actual data of the participant. Returns the logL for these parameter values, 
    the higher the logL, the better! Thus if want to minimize, take -logL and find minimum!"""
    # n_trials = data.shape[0]
    values = np.array([[0.5, 0.5], [0.5, 0.5]])
    Accuracy = (data['Response'] == data['CorResp'])[:n_trials]
    actual_rewards = np.array((Accuracy == data['FBcon'][:n_trials]))
    actual_choices = np.array(data['Response'][:n_trials])
    stimuli = np.array(data['Stimulus'])
    logL = 0
    for trial in range(n_trials): 
        stimulus = int(stimuli[trial])
        #The choice that was made at this trial and whether reward was received
        chosen_action = actual_choices[trial].astype(int)
        rew_this_trial = actual_rewards[trial]
        #calculate the probability of each choice at this trial given the Values
             #Values are updated with current_learning_rate
        stimulus_weights = values[stimulus, :]
        probabilities = softmax(current_values = stimulus_weights, temperature = used_temperature)
        current_likelihood = probabilities[chosen_action]
        logL = logL + np.log(current_likelihood)
        # print(current_likelihood)
        PE, updated_value = rescorla_wagner(previous_value = values[stimulus, chosen_action], 
                                                obtained_rew = rew_this_trial, 
                                                learning_rate = learning_rate_estimate) 
        values[stimulus, chosen_action] = updated_value
    return -logL



#%%

def normalize(Data = None): 
    Normalized_data = (Data - np.mean(Data)) / np.std(Data)
    return Normalized_data
