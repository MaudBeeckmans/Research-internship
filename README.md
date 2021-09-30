# research-internship

Explanation of the different files within this repository 
1. simple_RW_model.py:
- contains the formula's needed for the creation of a simple RW model 
  --> 'softmax': to make a decision using the softmax function, should define temperature (noise) and the values of the options at stake
  --> 'choose_option': to choose an option with a certain probability 
  --> 'rescorla_wagner': to compute the PE and value given a certain obtained_reward, previous_value (or expected reward) and learning_rate
- contains a short implementation of an RW model (simple 2-armed bandit task where reward is delivered with probability 0.2 and 0.8 
  
2.RW_simulation_EEGexp: 
- contains formula to simulate data as in the EEG experiment (from Verbeke et al., 2021)
- formula allows to simulate participants behaviour according to the RW model 
  --> have to define the 'learning_rate', 'temperature' (noise), 'design_file' (csv containing the design for a pp.) 
      and 'output_file' (where the csv file containing the simulated data will be stored)
