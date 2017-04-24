import numpy as np
from pandas import *

X = [[0],[1]]

A = ['GC', 'GD', 'PEEK'] #GuessClubs, GuessDiamonds, Peek

Z = ['OC','OD','NOTHING'] #ObserveClubs, ObserveDiamonds, Nothing
     

P_GC = np.array([[0.5, 0.5],
                 [0.5, 0.5]])
     
P_GD = np.array([[0.5, 0.5],
                 [0.5, 0.5]])

P_PEEK = np.array([[1, 0],
                    [0, 1]])
     
Z_GC = np.array([[0, 0, 1],
                 [0, 0, 1]])

Z_GD = np.array([[0, 0, 1],
                 [0, 0, 1]])
     
Z_PEEK = np.array([[0.9, 0.1, 0],
                 [0.1, 0.9, 0]])


C = np.array([[0,1,0.1],
            [1,0,0.1]])

random_policy =np.array([[1/3, 1/3, 1/3],
						[1/3, 1/3, 1/3]]);

pomdp = {"X": X, 
		"A": A, 
		"Pa's": [P_GC, P_GD, P_PEEK], 
		"C":C,
		"Z":Z, 
		"Pz's":[Z_GC, Z_GD, Z_PEEK]} 




def generateRandomTrajectory(POMDP, policy, s0, steps=100):  #only 100 for debugging
    gamma = 0.9
    states = np.array([s0])

    actions = np.array([])
    observations = np.array([])

    cost = 0
    
    for i in range(0, steps):
        random_action = np.random.choice(len(POMDP['A']), size=1, p=policy[states[i]])
        possible_state = np.random.choice(len(POMDP['X']), size=1, p=POMDP["Pa's"][random_action][states[i]])
        possible_observation = np.random.choice(len(POMDP['Z']), size=1, p=POMDP["Pz's"][random_action][states[i]])
        
        states = np.append(states, possible_state)
        actions = np.append(actions, random_action)
        observations = np.append(observations, possible_observation)

        #cost += MDP["C"][states[i]][random_action]*pow(gamma,i)
    
    print (states)
    print (actions)
    print (observations)

initial_state = 0

generateRandomTrajectory(pomdp,random_policy,initial_state)