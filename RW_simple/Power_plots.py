# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 08:21:05 2021

@author: Maud
"""

import pandas as pd
import numpy as np 
import os 
from matplotlib import pyplot as plt 
from scipy import stats as stat

N_pp = 40
N_trials = 3000
folder_name = 'Alpha_estimates'
participants = np.arange(0, N_pp, 1).astype(int)


input_file = os.path.join(os.getcwd(), folder_name)
input_DF = pd.read_csv(input_file + str('\DF_{}trials_{}pp.csv'.format(N_trials, N_pp)))
alpha_real  = input_DF['learning_rate']
alpha_est = input_DF['est_learning_rate']

#Power option A
cor = np.round(np.corrcoef(alpha_real, alpha_est)[0, 1], 2)
fig, axes = plt.subplots(nrows = 1, ncols = 1)
axes.plot(alpha_real, alpha_est, 'o')
axes.set_title('Correlation with {} trials and {} pp: {}'.format(N_trials, N_pp, cor))
axes.set_xlabel('real LR', loc = 'right')
axes.set_ylabel('esimated LR', loc = 'center')

#Power option B
realLR_G1 = alpha_real[:int(N_pp/2)]
realLR_G2 = alpha_real[int(N_pp/2):]
estLR_G1 = alpha_est[:int(N_pp/2)]
estLR_G2 = alpha_est[int(N_pp/2):]
T_stat_real, P_value_real = stat.ttest_ind(realLR_G1, realLR_G2) 
T_stat_est, P_value_est = stat.ttest_ind(estLR_G1, estLR_G2) 
print('P-value for real LR: {}, P-value for estimate LR: {}'.format(P_value_real, P_value_est))
