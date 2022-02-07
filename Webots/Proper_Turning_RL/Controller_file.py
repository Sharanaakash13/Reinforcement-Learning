from controller import Robot
from controller import DistanceSensor
from controller import Motor
from controller import Supervisor

from gym import Env
from gym.spaces import Box, Discrete
import numpy as np
import random 

# TIME_STEP = 64 




    
# robot = Robot()
supervisor = Supervisor()

timestep = int(supervisor.getBasicTimeStep())
print(timestep)
steps = 0
# What is the above command line:
# It counts the number of steps the agent takes with each input

CRUISING_SPEED = 10

TURN_SPEED = CRUISING_SPEED/4.0

# first activate the ultrasonic sensors
UltrasonicSensor = DistanceSensor('UltrasonicSensor')
UltrasonicSensor.enable(timestep)

# Just for verification print out the high and the low values of the ultrasonic sensor
print(UltrasonicSensor.getMinValue())
print(UltrasonicSensor.getMaxValue())
print(UltrasonicSensor.getValue())

# The observation space in this case will be the sensor reading of the ultrasonic sensor
observation_space = Box(low=np.array([UltrasonicSensor.getMinValue()]), 
                             high=np.array([UltrasonicSensor.getMaxValue()]), dtype=np.float64)

# Actions the robot can take: 1) Go straight, 2) Take a left turn, and lastly 3) Take a right turn
action_space = Discrete(3)
print(action_space.n)

episodeScore = 0     # score sccumulated during an episode
episodeScoreList = []


    
wheels = []
for wheelName in ['motor_1', 'motor_2', 'motor_3', 'motor_4']:
    wheel = supervisor.getDevice(wheelName)    # get the motor handle
    wheel.setPosition(float('inf'))    # Setting the starting position
    wheel.setVelocity(0.0)             # Zero out starting velocity
    wheels.append(wheel)
        
def get_observations():
    ultrasonicRead = UltrasonicSensor.getValue()
    return ultrasonicRead
   
def get_reward():
    if UltrasonicSensor.getValue() > 2.25:
        reward = +10
        
    else:
        # for every other value of the ultrasonic sensor we have a sensor reading of less than 1000's penalize it...
        reward = -10
    return reward
    
def is_done():
    # if self.stepsPerEpisode > 600:
        # done = True
    # else:
        # done = False
        
    # we can also define a hard constrain for the robot by defining a limit for it, in terms of the extent to which it can turn
    # so if the sensor reading is less than 950, which the rob ot is moving/ turning too much to the left or to the right
    if UltrasonicSensor.getValue() < 1:
        done = True
    else:
        done = False
    return done
    
def reset():
    robot_node = supervisor.getFromDef("MY_ROBOT")
    trans_field = robot_node.getField("translation")
    rotation_field = robot_node.getField("rotation")
    INITIAL = [0.01, 0.04, 3.4]
    # axis = [0, 1, 0]
    angle = 0
    trans_field.setSFVec3f(INITIAL)
    rotation_field.setSFRotation([0,0,1, angle])
    robot_node.resetPhysics()
    # supervisor.simulationReset()
    return UltrasonicSensor.getMaxValue()
    
# We haven't define any reset function:
# def reset(self):
    # pass    
    
def apply_action(action):
    if action == 0:    #  just go straight
        wheels[3].setVelocity(-CRUISING_SPEED)
        wheels[2].setVelocity(-CRUISING_SPEED)
        wheels[0].setVelocity(-CRUISING_SPEED)
        wheels[1].setVelocity(-CRUISING_SPEED)
        
    elif action == 1:    # maybe define a right turn over here
        wheels[3].setVelocity(CRUISING_SPEED)
        wheels[2].setVelocity(-CRUISING_SPEED)
        wheels[0].setVelocity(-CRUISING_SPEED)
        wheels[1].setVelocity(CRUISING_SPEED)
       
    elif action == 2:      # maybe we can define a left turn over here
        wheels[3].setVelocity(-CRUISING_SPEED)
        wheels[2].setVelocity(CRUISING_SPEED)
        wheels[0].setVelocity(CRUISING_SPEED)
        wheels[1].setVelocity(-CRUISING_SPEED)

def get_info():
    return None
    
# def render(self, mode='human'):
    # print("render() is not used")
    
def step(action):
# taking a step eventually means taking an action:
    apply_action(action)     # this will activate the action function
    return (
        get_observations(),
        get_reward(),
        is_done(),
        get_info(),
        )
            

#########################################
# Define all the constants related to reinforcement learning over here:
#########################################

LEARNING_RATE = 0.5
DISCOUNT = 0.95     # this is the discount, the factor by which we hugely discount the future reward points
EPISODES =1000     # Number of episodes we will make the agent go through, until its well leanred how to navigate through the provided environment

# For the time being we will not discritize the states of the agent(in this reinforcement learning problem we are computing the distance value from the sensor as the state of the agent in the environment)
# Define the observation space size depending on the discritization we form:
print(len(observation_space.high))
DISCRETE_OS_SIZE = [200] * len(observation_space.high)
print(DISCRETE_OS_SIZE)
# Also defining the window size of the discrete states:
discrete_os_win_size = (observation_space.high - observation_space.low)/ DISCRETE_OS_SIZE
print(discrete_os_win_size)
######################################################################
# Define the exploration factor of the agent, whose value decays as we take each steps in a particular environment
#EPSILON = 0.9 # exploration factor is basically a decision making factor as to whether explore the environment more or exploit the already known things about the environment

# Specify the first episode when the epsilon decay should start and also when it should be ending
#START_EPSILON_DECAYING = 1
#END_EPSILON_DECAYING = EPISODES    # keep the decaying of the exploration factor on until the last episode

# Formulation to evaluate by what factor the epsilon value should get decayed:
#epsilon_decay_value = EPSILON/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)
# What this above 2 command lines mean is the observation space of the ultrasonic readings is divided into 500 equal parts having some sort of ranges
##################################################################
epsilon=0; #initializing epsilon
epsilon_max=1; #Max epsilon value
epsilon_min=0.01; # Min Epsilon value
epsilon_decay_rate=0.001 #Courtesy of Mathworks

# Now let's create a q-table that's filled up randomly with random number, which would be later updated according to the rewards earned by the agent
q_table = np.random.uniform(low = -10, high = 10, size = ([DISCRETE_OS_SIZE[0]+1] + [action_space.n]))
#q_table=np.loadtxt('q_table_new_3actions.txt',dtype=int)
# So, think of the q_table as a form of table, where in the states represents the position of the agent in the environment and the corresponding action the agent is capable of taking at that time step
# low is the minimum reward it can earn and high is the maximum reward it can earn

# convert the states(in this case the readings from the ultrasonic sensor into discrete states)
def get_discrete_state(state):
    discrete_state = (state - observation_space.low)/ discrete_os_win_size
    return tuple(discrete_state.astype(np.int))


ep_rewards=[]
epsilon_record=[]
for episode in range(0, EPISODES):
    discrete_state = get_discrete_state(reset())     # the reset function is not defined anywhere its printing none as the output:
    
    # print(state)
    done = False
    score = 0
    
    while not done:
        supervisor.step(timestep)
        
        # Now let's define the epsilon-greedy function to randomly or greedily choose an action:
        if np.random.random() > epsilon:
            action = np.argmax(q_table[discrete_state])
        else:
            action = np.random.randint(0, action_space.n)
        
        # action = 0
        new_state, reward, done, info = step(action)
        # print(new_state)
        score+=reward
        
        # converting the new state into a discrete state:
        new_discrete_state = get_discrete_state(new_state)
        print(new_discrete_state)
        # if not done in the current step:
        if not done:
            # new_discrete_state-=1
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action, )]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state+(action, )] = new_q
        else:
            q_table[discrete_state+(action, )] = 0
            
        discrete_state = new_discrete_state
        
    # the epsilon value gets decayed in the next episode:
    #if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        #EPSILON -= epsilon_decay_value
    # ep_rewards.append(episode_reward)
    if epsilon>epsilon_min:
        epsilon=epsilon*(1-epsilon_decay_rate) 
            
    ep_rewards.append(score)       
    print('Episode:{} Score:{}'.format(episode, score))
    np.savetxt('q_table_new.txt',q_table,fmt='%d')
    np.savetxt('reward_array.txt',ep_rewards,fmt='%d')

    
    
    
    
    
    
    
    
    
    
    