import warnings
warnings.filterwarnings("ignore")
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



#pergunta 2

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

    return [states, actions, observations]

initial_state = 0

[states, actions, observations] = generateRandomTrajectory(pomdp,random_policy,initial_state)


#end pergunta 2

#pergunta3
def beliefUpdate(POMDP, belief, action, observation):
	
	a1_hat = np.dot(belief, POMDP["Pa's"][int(action)])
	diag = np.diagflat(POMDP["Pz's"][int(action)][:,int(observation)])
	a1 = np.dot(a1_hat, diag)
	norm_a1 = a1 / np.sum(a1)

	return norm_a1

#beliefUpdate(pomdp, np.array([0.5,0.5]), 2,0)


def existsInList(elem, lista):
	for i in range(0,len(lista)):	
		dist = np.linalg.norm(lista[i]-elem)
		if (lista[i][0] == elem[0]) and (lista[i][1] == elem[1]) or dist < 1e-5:
			return True
	return False


def computeBeliefSequence(POMDP, initial_belief, actions, observations):

	input_belief = initial_belief
	beliefs = np.array([initial_belief])

	for i in range(0,len(actions)):

		new_belief = beliefUpdate(pomdp, input_belief, actions[i],observations[i])

		if not existsInList(new_belief, beliefs):
			beliefs = np.append(beliefs, [new_belief],axis=0)
			

		input_belief = new_belief
		#print (input_belief)
	print (beliefs)
	return beliefs

beliefs = computeBeliefSequence(pomdp,np.array([0.5,0.5]), actions, observations)

#end3