# Reinforcement-Learning
This project is all about planning a path using Reinforcement Learning. 

This project involves three modules
* Reinforcement learning algorithm
* Ultra-sonic sensor module - Input sensor to detect obstacle
* Micro-controller module - Ardunio


### Description of the Reinforcement learning script
* The python script is an implementation of reinforcement learning, specifically Q-learning, for a smart car. The car has an ultrasonic sensor to detect obstacles, and it can take three actions: go straight, turn left, or turn right. The code uses the gym library to define the observation and action spaces. The smart car class contains the following methods:

* **__init__(self)**: initializes the smart car object and the ultrasonic sensor module.
* **get_observations(self)**: reads the current distance from the ultrasonic sensor and returns it.
* **get_reward(self)**: calculates the reward based on the current distance from the ultrasonic sensor.
* **is_done(self, stepsPerEpisode)**: determines if the episode is over based on the current distance and the number of steps taken.
* **reset(self)**: resets the environment to its initial state.
* **apply_action(self, action)**: applies the specified action to the smart car.
* **get_info(self)**: returns any additional information about the environment.
* **get_discrete_state(self, state)**: discretizes the current state based on the number of discrete states defined.
* **step(self, actionValue)**: applies the specified action to the smart car, gets the new state, calculates the reward, and determines if the episode is over.
* The code also defines several constants related to reinforcement learning, such as the learning rate, the discount factor, the number of episodes, and the number of discrete states. 
* It initializes the Q-table randomly and then rewrite the Q-table as it learns by itself. 
* The training loop iterates over the specified number of episodes, applies the Q-learning algorithm to update the Q-table, and saves the updated Q-table at the end of each episode. 
* Finally the exploration rate starts high and decays linearly until the end of the training.
