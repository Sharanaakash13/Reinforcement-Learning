import numpy as np
import random 
import time
import sys
from gym import Env
from gym.spaces import Box, Discrete

from FindDistance import FindDistance # Module 1 ultrasonic 
import Arduino  # Module 2 Arduino


# Observation space dependent on the sensor reading of the ultrasonic sensor
observation_space = Box(low=np.array([0]), 
                             high=np.array([400]), dtype=np.float64)

# Actions the robot can take: 1) Go straight, 2) Take a left turn, and lastly 3) Take a right turn
action_space = Discrete(3)
print(action_space.n)

episodeScore = 0     # score sccumulated during an episode
episodeScoreList = []


class smartCar:
	def __init__(self):
		############## Read distance with ultrasonic sensor  ################
		sonar = FindDistance()  # Accessing ultrasonic reading
		self.ultrasonic = sonar.get_distance()

		# Also defining the window size of the discrete states:
		self.discrete_os_win_size = (observation_space.high - observation_space.low) / 200
		print(discrete_os_win_size)

	def get_observations(self):
		############## INSERT MODULE 1 HERE #############
		distance = self.ultrasonic		
		print(distance)  
		return distance #return distance(cm) from sensor

	def get_reward(self):
		if distance >= 250:
			reward_s = +10
		elif distance in range(25, 249):
			reward_s = 2
		else:
			reward_s = -10

		print('Reward for step taken: {}'.format(reward))
		return reward_s

	def is_done(self, stepsPerEpisode):
		############### Episode ends in case of 25 actions ###############
		if stepsPerEpisode > 25:
			done_s = True
		elif distance < 5:       # to avoid coliision
			done_s = True
		else:
			done_s = False

		return done_s

############# Episode ends in case of collision
#	    	if distance < 10:
#			done = True
#	   	 else:
#			done = False
#	    	return done

	def reset(self):
		# Adding some kind of time delay between picking up robot and placing in original location
		for second in range(50, 0, -1):
			sys.stdout.write('\r')
			sys.stdout.write('{:2d} seconds remaining.'.format(second))
			sys.stdout.flush()
			time.sleep(1)


			# ############ Insert Module 1 here ############# this will output distance
			# # Reading Initial State
			# print(self.ultrasonic)
	   		# return self.ultrasonic # Returns state of the reset location
	    
	def apply_action(self, action):
		if action == 0:    #  just go straight
			steer ='No steer'
		elif action == 1:    # maybe define a right turn over here
			steer = 'Steer Right'
		elif action == 2:     # maybe we can define a left turn over here
			steer = 'Steer Left'

		print('Action taken : {}'.format(steer))
		#Use Module 3 for arduino communication
		Arduino.apply_action(action)

	def get_info(self):
		return None

	def get_discrete_state(self, state):
		# convert the states(in this case the readings from the ultrasonic sensor into discrete states)
		discrete_s = state / self.discrete_os_win_size  # converting from real-reading to discretized reading
		return tuple(discrete_s.astype(np.int))

	def step(self, actionValue):
		# taking a step eventually means taking an action:
		apply_action(actionValue)     # this will activate the action function
		return (
		get_observations(),
		get_reward(),
		is_done(),
		get_info(),
		)

#########################################
# Define all the constants related to reinforcement learning over here:

########################################

LEARNING_RATE = 0.1
DISCOUNT = 0.95     # this is the discount, the factor by which we hugely discount the future reward points
EPISODES = 1000    # Number of episodes we will make the agent go through, until its well leanred how to navigate through the provided environment
NUM_OF_STATES = 200

#Discretizes the ultrasonic sensor readings into 200 states (2cm / state)
DISCRETE_OS_SIZE = [NUM_OF_STATES] * len(observation_space.high)
print(DISCRETE_OS_SIZE)

############### EXPLORATION RATE ###############
EPSILON = 0.9 # exploration factor: exploration vs exploitation

# Specify the first episode when the epsilon decay should start and also when it should be ending
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES    # keep the decaying of the exploration factor on until the last episode

# Formulation to evaluate by what factor the epsilon value should get decayed:
epsilon_decay_value = EPSILON/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

############### LOAD Q-TABLE TRAINED IN WE-BOTS ###############

# Initializing the q table randomly
# q_table = np.random.uniform(low = -10,
# 							high = 10, size = ([DISCRETE_OS_SIZE[0]+1] + [action_space.n]))

# Initializing the q table from Webots
# Loading trained q table
q_table = np.loadtxt('Q_table.txt', dtype=int)

############### TRAINING LOOP ###############
episodes = 200
ep_reward = []

for episode in range(0, episodes):
	# Countdown to reset the smart car
	smartCar.reset()

	# Gets the initial state(distance measured)
	discrete_state = smartCar.get_discrete_state(smartCar.get_observations())     #Reset() function called - will start with time-delay

	done = False
	score = 0

	############### Episode loop starts here ###############
	while not done:
	# Now let's define the epsilon-greedy function to randomly or greedily choose an action:
		if np.random.random() > EPSILON:
			action = np.argmax(q_table[discrete_state]) #when epsilon has sufficiently decayed, it will start exploitation
        else:
            action = np.random.randint(0, action_space.n)
        
        # action = 0
        new_state, reward, done, info = smartCar.step(action)
        # print(new_state)
        score+=reward
        
        # converting the new state into a discrete state:
        new_discrete_state = smartCar.get_discrete_state(new_state)
        print(new_discrete_state)

		if not done:
			#new_discrete_state-=1
			max_future_q = np.max(q_table[new_discrete_state])
			current_q = q_table[discrete_state + (action, )]
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
			q_table[discrete_state+(action, )] = new_q
    	else:
            q_table[discrete_state+(action, )] = 0
            
        discrete_state = new_discrete_state
		############### Episode loop ends here ###############

    # the epsilon value gets decayed in the next episode:
	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		EPSILON -= epsilon_decay_value

	# Storing total reward for every episode
	ep_rewards.append(score)
	print('Episode:{} Score:{}'.format(episode, score))

	# Saving the Q table as .txt file
	np.savetxt('Q_table.txt',q_table,fmt='%d')
	# Saving the score as a .txt file
	np.savetxt('Episode_Score.txt',score,fmt='%d')

print('Final q table :/n{}'.format(q_table))


