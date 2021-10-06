# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:23:38 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 

#I generated the dataset under a different letter each time 
letters = ['A', 'B', 'C', 'D', 'Z']
data_dir =  os.path.join(os.getcwd(), "Simulated_datasets")

for letter in letters: 
    data_all_pp = pd.read_csv(data_dir + '\simulated_data' + letter + '.csv', header = None)
    data_all_pp = data_all_pp.values
    all_p_values = pd.read_csv(data_dir + '\p_simulations' + letter + '.csv', header = None)
    n_pp = all_p_values.shape[0]
    all_p_values = all_p_values.values.reshape(n_pp)
    #print(all_p_values)
    
    mean_G1 = np.round(np.mean(all_p_values[:int(n_pp/2)]), 2)
    mean_G2 = np.round(np.mean(all_p_values[int(n_pp/2):]), 2)
    diff = np.round(mean_G2-mean_G1, 2)
    std1 = np.round(np.std(all_p_values[:int(n_pp/2)]), 2)
    std2 = np.round(np.std(all_p_values[int(n_pp/2):]), 2)
    
    print("\n\nmean G1 = {}, mean G2 = {}; difference = {}\nstd G1 = {}, stdG2 = {}"
          .format(mean_G1, mean_G2, diff, std1, std2))


#%% 

"""Create dataset with 80 pp: combination of the 4 datasets previously used"""
p_80pp_g1 = np.array([])
p_80pp_g2 = np.array([])

for letter in letters: 
    data_all_pp = pd.read_csv(data_dir + '\simulated_data' + letter + '.csv', header = None)
    data_all_pp = data_all_pp.values
    all_p_values = pd.read_csv(data_dir + '\p_simulations' + letter + '.csv', header = None)
    all_p_values = all_p_values.values.reshape(n_pp)
    data_group1 =  data_all_pp[:10, :]
    data_group2 =data_all_pp[10:, :]
    p_group1 = all_p_values[:10]
    p_group2 = all_p_values[10:]
    if letter == 'A': 
        data_80pp_g1 = data_group1
        data_80pp_g2 = data_group2
    else: 
        data_80pp_g1 = np.row_stack([data_80pp_g1, data_group1])
        data_80pp_g2 = np.row_stack([data_80pp_g2, data_group2])
    
    p_80pp_g1 = np.append(p_80pp_g1, p_group1)
    p_80pp_g2 = np.append(p_80pp_g2, p_group2)
    
data_80pp = np.row_stack([data_80pp_g1, data_80pp_g2])
p_80pp = np.concatenate([p_80pp_g1, p_80pp_g2])


pd.DataFrame(data_80pp).to_csv("simulated_dataZ.csv", header = None, index = None)
pd.DataFrame(p_80pp).to_csv("p_simulationsZ.csv", header = None, index = None)







