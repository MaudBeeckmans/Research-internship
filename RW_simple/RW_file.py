from Simulate_data import generate_parameters, simulate_data
from Estimate_likelihood import likelihood
import numpy as np
import pandas as pd
import os 

HPC = True #Defines the correct directory to store the data 
test = False # should be True when testing on own laptop or in interactive qsub 
#%%Simulate data
mean_alpha1 = 0.3
mean_alpha2 = 0.2
std_alpha = 0.05
N_pp = 40
N_trials = 3000

learning_rates_G1 = generate_parameters(mean = mean_alpha1, std = std_alpha, n_pp = int(N_pp/2)) 
learning_rates_G2 = generate_parameters(mean = mean_alpha1, std = std_alpha, n_pp = int(N_pp/2))
Learning_rates = np.concatenate([learning_rates_G1, learning_rates_G2])
Temperatures = np.ones(N_pp)

DF_all_pp = simulate_data(learning_rates = Learning_rates, temperatures = Temperatures, 
                          n_trials = N_trials)

#%%
participants = np.arange(0, N_pp, 1).astype(int)
if test == True: 
    participants = np.array([0, 1]).astype(int)
alpha_estimates = np.array([])
for pp in participants: 
    alpha_range = np.round(np.arange(0.1, 1, 0.01), 3)
    if test == True: 
        alpha_range = np.round(np.arange(0.1, 1, 0.1), 3)
    all_logL = np.array([])
    for alpha in alpha_range:
        logL = likelihood(learning_rate_estimate = alpha, temperature_estimate = 1, 
                          actual_choices = DF_all_pp['choices'][pp], 
                          actual_rewards = DF_all_pp['rewards'][pp], 
                          start_values = np.array([0.5,0.5]))
        all_logL = np.append(all_logL, -logL)
        # print("\n\n\n")
        
        # print("Likelihood for alpha {} is {}".format(alpha, -logL))
    alpha_estimate = alpha_range[np.argmin(all_logL)]
    alpha_estimates = np.append(alpha_estimates, alpha_estimate)
    print("real_LR = {}; est_LR = {} for pp {}".format(DF_all_pp['learning_rate'][pp], 
                                                       alpha_estimate, pp))
DF_all_pp['est_learning_rate'] = alpha_estimates

if HPC == True: 
    data_dir = os.environ.get('VSC_DATA')
    df_dir = data_dir + '/RW_simple/Data'
    if not os.path.isdir(df_dir): 
        os.mkdir(df_dir)
else: 
    df_dir= os.getcwd()
DF_all_pp.to_csv(df_dir + str("/DF_{}trials_{}pp.csv".format(N_trials, N_pp)))
