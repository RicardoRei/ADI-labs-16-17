import numpy as np


#################(A)#################
StateSpace = np.array([['0,0', '0,1', '0,2', '0,3', '0,4', 
						'1,0', '1,1', '1,2', '1,3', '1,4', 
						'2,0', '2,1', '2,2', '2,3', '2,4']])  #lines x rows

ActionSpace = np.array([["U", "D", "L", "R"]])

					#	 U	  D	   L 	R
CostMatrix = np.array([[1.0, 1.0, 1.0, 1.0],   		#00
					   [1.0, 1.0, 1.0, 1.0],		#01
					   [1.0, 1.0, 1.0, 1.0],		#02
					   [1.0, 1.0, 1.0, 1.0],		#03
					   [1.0, 0.0, 1.0, 1.0],		#04
					   [1.0, 1.0, 1.0, 1.0],		#10
					   [1.0, 1.0, 1.0, 1.0],		#11
					   [1.0, 1.0, 1.0, 1.0],		#12
					   [1.0, 1.0, 1.0, 1.0],		#13
					   [1.0, 1.0, 1.0, 1.0],		#14
					   [1.0, 1.0, 1.0, 1.0],		#20
					   [1.0, 1.0, 1.0, 1.0],		#21
					   [1.0, 1.0, 1.0, 1.0],		#22
					   [1.0, 1.0, 1.0, 0.0],		#23
					   [0.0, 1.0, 1.0, 1.0]])		#24



#################(B)#################
GAMMA = 0.95
InitialState = StateSpace[0][5]
print (InitialState)

Action = ActionSpace[0][3]
print (Action)

InformationAction1 = [InitialState, Action, CostMatrix[5][3], StateSpace[0][6]]
print (InformationAction1)

InformationAction2 = [InformationAction1[3], Action, CostMatrix[6][3], StateSpace[0][2]]
print (InformationAction2)


#################(C)#################
		  #  	U    D	  L    R
Q = np.array([[0.0, 0.0, 0.0, 0.0],   	#00
              [0.0, 0.0, 0.0, 0.0],		#01
			  [0.0, 0.0, 0.0, 0.0],		#02
			  [0.0, 0.0, 0.0, 0.0],		#03
			  [0.0, 0.0, 0.0, 0.0],		#04
			  [0.0, 0.0, 0.0, 0.0],		#10
			  [0.0, 0.0, 0.0, 0.0],		#11
			  [0.0, 0.0, 0.0, 0.0],		#12
			  [0.0, 0.0, 0.0, 0.0],		#13
			  [0.0, 0.0, 0.0, 0.0],		#14
			  [0.0, 0.0, 0.0, 0.0],		#20
			  [0.0, 0.0, 0.0, 0.0],		#21
			  [0.0, 0.0, 0.0, 0.0],		#22
			  [0.0, 0.0, 0.0, 0.0],		#23
			  [0.0, 0.0, 0.0, 0.0]])	#24


def q_update(infoState):
	xt = infoState[0]
	at = infoState[1]
	ct = infoState[2]
	xt1 = infoState[3]
	indAt = np.where(ActionSpace[0]==at)[0][0]
	indXt = np.where(StateSpace[0]==xt)[0][0]
	indXt1 = np.where(StateSpace[0]==xt1)[0][0]

	mini = min(Q[indXt1,:])
	Q[indXt][indAt] = Q[indXt][indAt] + 0.1 * (ct + GAMMA * mini - Q[indXt][indAt]) 

q_update(InformationAction1)
print (Q)

q_update(InformationAction2)
print(Q)




#print(InformationAction1)
#print(InformationAction2)


