# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:31:59 2021

@author: Maud
"""

"""Update: RW-model with 4 weight / values 
    - weights for each stimulus - action pair 
        --> 4 weights: stimA + L resp; stim A + R resp; stim B + L resp; stim B + R resp 
    - depending on which stimulus is shown, then only 2 weights (values) are of importance """

import numpy as np
import pandas
from psychopy import data , os
from Simple_RW_model import softmax, choose_option, rescorla_wagner


def simulate_RW(learning_rate = 0.5, temperature = 1, design_file = 'Data0.csv', data_file = 'Simulation.csv'): 

    design_path = "C:\\Users\\Maud\\Documents\\Psychologie\\2e master psychologie\\Research Internship\\Start to model RI\\Maud_Sims\\Data_to_fit\\"
    design_DF = pandas.read_csv(design_path + design_file)
    design_DF.columns = ['Trial_number', 'Rule', 'Stimulus', 'Response', 'CorResp', 
                         'FBcon', 'Expected value','PE_estimate', 'Response_likelihood', 'Module']
    design = design_DF.to_numpy()
    #design = np.column_stack([design, np.zeros([480, 2])])
    
    output_map = 'Simulations_trying_phase'
    my_output_directory = os.getcwd() + '/' + output_map
    if not os.path.isdir(my_output_directory): 
            os.mkdir(my_output_directory)
    output_file = data_file
    
    n_trials = design.shape[0]
    alpha = learning_rate
    gamma = temperature
    rew_per_trial = 10 #how much you gain on a rewarded trial 
    #important: values zijn voor de rules! Welke rule wil pp. uitvoeren 
    n_actions = 2
    n_stim = 2
    values = np.random.uniform(size = (n_stim, n_actions))
    prev_rule = 0
    total_reward = 0
    
    for trial in range(n_trials): 
        
        #define the variables you'll need for this trial (take them from the design_array)
        rule = design[trial, 1]
        stimulus = np.int(design[trial, 2])
        CorResp =  np.int(design[trial, 4])
        FBcon = design[trial, 5]
        
        if trial == 0 or rule != prev_rule:
            print("\n\nRule changed; current rule is {}".format(rule))
        
        #define which weights are of importance on this trial (depending on which stimulus was shown)
        stimulus_weights = values[stimulus, :]
        # compute probability of each action on this trial (using the weights for each action with the stimulus of this trial)
        action_probabilities = softmax(current_values = stimulus_weights, temperature = gamma)
        # define which action is chosen (based on the probabilities)
        chosen_action = choose_option(prob = action_probabilities)
        #define whether reward was received this trial or not
        rew_present = ((chosen_action == CorResp and FBcon == 1) or (chosen_action!= CorResp and FBcon == 0))*1
        rew_this_trial = rew_present * rew_per_trial
        #compute the PE and the updated value for this trial (and this stimulus-action pair)
        PE, updated_value = rescorla_wagner(previous_value = values[stimulus, chosen_action], 
                                            obtained_rew = rew_this_trial, learning_rate = alpha)
        
        #store the relevant variables in the array
        #store the response given on this trial 
        design[trial, 3] = chosen_action
        #first store the value for this trial before the value is updated
        design[trial, 6] = values[stimulus, chosen_action]
        #Store the PE on this trial (is related to the choice you made)
        design[trial, 7] = PE
        #Store the probability for the choise that you made on this trial 
        design[trial, 8] = action_probabilities[chosen_action]
        
        #update the value of the stimulus-action that was relevant this trial 
        values[stimulus, chosen_action] = updated_value
        
        
        prev_rule = rule
        total_reward = total_reward + rew_this_trial
        #print("Action = {}, Stimulus = {}; Rew = {}; updated values are {}".format(chosen_action, stimulus, rew_present, values))
        
    
    np.savetxt(output_file, design, delimiter = ',', fmt = "%.3f",
              header = 'Trial_number,Rule,Stimulus,Response,CorResp,FBcon,Expected value,PE_estimate,Response_likelihood,Module,Value_rule0,Value_rule1')
    return total_reward


total_reward = simulate_RW(learning_rate = 0.5, temperature = 1)
print(total_reward)
