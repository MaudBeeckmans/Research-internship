# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:31:59 2021

@author: Maud
"""

import numpy as np
import pandas
from psychopy import data , os
from Simple_RW_model import softmax, choose_option, rescorla_wagner

design_path = "C:\\Users\\Maud\\Documents\\Psychologie\\2e master psychologie\\Research Internship\\Start to model RI\\Maud_Sims\\Data_to_fit\\"
design_DF = pandas.read_csv(design_path + "Data" + str(0) + ".csv")
design_DF.columns = ['Trial_number', 'Rule', 'Stimulus', 'Response', 'CorResp', 
                     'FBcon', 'Expected value','PE_estimate', 'Response_likelihood', 'Module']
design = design_DF.to_numpy()
design = np.column_stack([design, np.zeros([480, 2])])

output_map = 'Simulations_trying_phase'
my_output_directory = os.getcwd() + '/' + output_map
if not os.path.isdir(my_output_directory): 
        os.mkdir(my_output_directory)
output_file = 'Simulation'

n_trials = design.shape[0]
alpha = 0.1
gamma = 1
rew_per_trial = 1 #how much you gain on a rewarded trial 
#important: values zijn voor de rules! Welke rule wil pp. uitvoeren 
values = np.array([0.0, 0.0])
prev_rule = 0

for trial in range(n_trials): 
    #define the variables you'll need for this trial (take them from the design_array)
    rule = design[trial, 1]
    stimulus = design[trial, 2]
    CorResp =  design[trial, 4]
    FBcon = design[trial, 5]
    if rule != prev_rule:
        print("\n\n\nRule changed")
    #print(trial, rule, stimulus, CorResp, FBcon)
    # compute the probability of each rule to be chosen this trial
    probabilities = softmax(current_values = values, temperature = gamma)
    # define which rule is chosen (based on the probabilities)
    choice = choose_option(prob = probabilities)
    print("Choice (implemented rule) on this trial is {}".format(choice))
    # rew_present contains whether there was reward present on this trial or not 
        # depends on whether the correct rule was implemented or not, doesn't depend on whether you answered left / right!
    rew_present = ((choice == rule and FBcon == 1) or (choice != rule and FBcon == 0))*1
    print("Correct rule is {}, FBcongruency is {}, so reward present? {}".format(rule, FBcon, rew_present))
    rew_this_trial = rew_present * rew_per_trial
    PE, updated_value = rescorla_wagner(previous_value = values[choice], 
                                        obtained_rew = rew_this_trial, learning_rate = alpha)
    #store the relevant variables in the array
    #first store the value for this trial before the value is updated
    design[trial, 6] = values[choice]
    #Store the PE on this trial (is related to the choice you made)
    design[trial, 7] = PE
    #Store the probability for the chose that you made on this trial 
    design[trial, 8] = probabilities[choice]
    #store the module you implemented (the rule that you used)
    design[trial, 9] = choice
    
    values[choice] = updated_value
    
    design[trial, 10:12] = values
    
    prev_rule = rule
    
    
    
    print(values)

np.savetxt("Simulations.csv", design, delimiter = ',', fmt = "%f",
          header = 'Trial_number,Rule,Stimulus,Response,CorResp,FBcon,Expected value,PE_estimate,Response_likelihood,Module,Value_rule0,Value_rule1')
    
    
    
    
    







# thisExp = data.ExperimentHandler(dataFileName = my_output_directory + output_file)
# DesignTL = pandas.DataFrame.to_dict(design_DF, orient = "records")
# trials = data.TrialHandler(trialList = DesignTL, nReps = 1, method = "sequential")
# thisExp.addLoop(trials)

# for trial in trials: 
#     print(type(trial['Trial_number']))    
#     thisExp.nextEntry()

# thisExp.saveAsWideText(my_output_directory + output_file + '.csv')
    
    