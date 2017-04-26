import warnings
warnings.filterwarnings("ignore")
import numpy as np
import time
from pandas import *

#pergunta1
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


#----------------------------------------------------------------------------------------------



#pergunta 2
def generateRandomTrajectory(POMDP, policy, s0, steps=1):  #only 100 for debugging
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
    
    #print (states)
    #print (actions)
    #print (observations)

    return [states, actions, observations]

initial_state = 0

[states, actions, observations] = generateRandomTrajectory(pomdp,random_policy,initial_state)




#----------------------------------------------------------------------------------------------



#pergunta3
def beliefUpdate(POMDP, belief, action, observation):
	
	a1_hat = np.dot(belief, POMDP["Pa's"][int(action)])
	diag = np.diagflat(POMDP["Pz's"][int(action)][:,int(observation)])
	a1 = np.dot(a1_hat, diag)
	norm_a1 = a1 / np.sum(a1)

	return norm_a1

#beliefUpdate(pomdp, np.array([0.5,0.5]), 2,0)


def existsInList(elem, lista):  #only works for 2d arrays
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



#----------------------------------------------------------------------------------------------







#pergunta4
gamma=0.9
def policyIteration(POMDP):
    pi = np.ones((len(POMDP['X']), len(POMDP['A']))) /2
    quit = False
    i = 0
    
    while not quit:
        
        #initialize cπ and pπ with first line of pi multiplyed by the costs for the first action
        cpi = np.diag(pi[:,0]).dot(POMDP["C"][:,[0]])
        ppi = np.diag(pi[:, 0]).dot(POMDP["Pa's"][0])
        
        # loop over the rest of the actions 
        for a in range(1, len(POMDP["A"])):
            cpi += np.diag(pi[:,a]).dot(POMDP["C"][:,[a]])
            ppi += np.diag(pi[:, a]).dot(POMDP["Pa's"][a])

        J = np.linalg.inv(np.eye(len(POMDP["X"])) - gamma * ppi).dot(cpi)
        
        Qa = [None] * len(POMDP["A"])
        
        # loop over every action
        for a in range(0, len(POMDP["A"])):
            Qa[a] = POMDP["C"][:,[a]] + gamma * POMDP["Pa's"][a].dot(J)
        
        pinew = np.zeros((len(POMDP['X']), len(POMDP['A'])))
        
        # loop over every action
        for a in range(0, len(POMDP["A"])):
            pinew[:, a, None] = np.isclose(Qa[a], np.min(Qa, axis=0), atol=1e-8, rtol=1e-8).astype(int)

        pinew = pinew / np.sum(pinew, axis=1, keepdims=True)
        quit = (pi == pinew).all()
        pi = pinew
        i +=1
    return (pi, i)

time_before = time.time()
optimal_policy, iterations = policyIteration(POMDP=pomdp)
time_after = time.time()
#print (optimal_policy)
#print ("number of iterations required: %d" % (iterations))
#print ("computation time required: %f"% (time_after - time_before))




#@brief: 
#      This function computes the valueIteration algorithm to find the optimal cost to go J*.
#
#@param: - MDP (as explained in activity 1)
#        - tolerance, which is used to stop the algorithm when Jnew and J are close by a small factor
#        - gamma, which represents the inflation.
#
#@return: 
#        returns a tuple that contains J* and the number of iterations required to compute J*
def valueIteration(POMDP, tolerance, gamma):
    
    ############################## AUXILIAR ############################################
    #@brief:
    #      computes Jnew.
    #
    #@param: - Qa, is a vector with the Q for every action.
    #
    #@return: 
    #       returns a column vector with the minimun value in every line of Qa.
    def computeJnew(Qa):
        Jnew = np.zeros((len(Qa[0]),1))
        for i in range(0, len(Qa[0])):
            min = Qa[0][i]
            for j in range(1, len(Qa)):
                if Qa[j][i] < min:
                    min = Qa[j][i]
            Jnew[i][0] = min
        return Jnew
    ####################################################################################
    
    J = np.zeros((len(POMDP["X"]), 1)) # initialize J
    err = 1
    i=0
    while err > tolerance:
        
        Qa = [None]*len(POMDP["A"]) #initialize empty list for Q values for actions a in A
        
        # loop over actions and compute Qa
        for a in range(0, len(POMDP["A"])):
            Qa[a] = POMDP["C"][:,[a]] + gamma * POMDP["Pa's"][a].dot(J)
        
        Jnew = computeJnew(Qa)
        err = np.linalg.norm(Jnew - J)
        i += 1
        J = Jnew    
    return (J, i)

time_before = time.time()
J_optimal, iterations = valueIteration(POMDP=pomdp, tolerance=1e-8, gamma=0.9)
time_after = time.time()

labels = ["00", "01"]
#print (DataFrame(J_optimal.T[0], index=labels, columns=["J optimal"]))
#print ("number of iterations required: %d" % (iterations))
#print ("computation time required: %f"% (time_after - time_before))


#---------------------------------------------------------------------

#pergunta5

def mlsHeuristic(belief,policy):
	index = np.argmax(belief)
	action = np.argmax(policy[index])
	return action

def avHeuristic(belief,policy):
    return 0

def QMDPHeuristic(belief,policy):
    gamma = 0.9
    Cpi = calculate_Cpi(pomdp["C"],policy)
    print("CPI")
    print(Cpi)

    Ppi = transition_Probabilities_For_Policy(pomdp, policy)
    print("PPI")
    print(Ppi)

    Jpi = np.dot(np.linalg.inv((np.identity(2)-(gamma*Ppi))), Cpi)
    print("JPI")
    print(Jpi)

    Qa = [None]*len(pomdp["A"])
    for a in range(0, len(pomdp["A"])):
            right = gamma * pomdp["Pa's"][a].dot(Jpi)
            print ("right")
            print (right)
            Qa[a] = pomdp["C"][:,[a]] + right
            print ("Qa:")
            print (Qa[a])
            

    result = np.dot(belief,Qa)

    print ("result:")
    print (result)
    index = np.argmin(result)
    return index


def useHeuristic(beliefs, heuristic, policy):
    actions = np.array([])
    for belief in beliefs:
        actions = np.append(actions,heuristic(belief,policy))
    print (actions)
		


def calculate_Cpi(costs, policy):
    cpi = np.zeros(len(policy))
   
    # loop over states
    for i in range(0, len(policy)):        
        # loop over actions to compute sum(pi(a|x) * c(a,x))

        sum = 0
        for j in range(0, len(costs[0])):
            sum += policy[i][j]*costs[i][j]

        cpi[i] = sum
    return cpi

def transition_Probabilities_For_Policy(POMDP, policy):
    Ppi = np.zeros((len(POMDP["X"]),len(POMDP["X"]))) # creates a matrix NxN where N is the size of X
    
    for i in range(0, len(POMDP["X"])):
        for j in range(0, len(POMDP["X"])):
            
            # for every entry we need to loop over possible actions to compute ∑ π(a|x)*P(y|x,a)
            sum = 0
            for k in range(0,len(POMDP["A"])):
                sum += policy[i][k] * POMDP["Pa's"][k][i][j]
            
            Ppi[i][j] = sum
    return Ppi

print ("Policy:")
print (optimal_policy)

useHeuristic(beliefs,QMDPHeuristic,optimal_policy)


