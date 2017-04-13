import numpy as np
from pandas import *

def normalizeMatrix(matrix):
	sum = 0
	for i in range(0, len(matrix)):
		for j in range(0, len(matrix[i])):
			sum += matrix[i][j]

		for j in range(0, len(matrix[i])):
			if matrix[i][j] > 0.0:
				matrix[i][j] = matrix[i][j]/sum
		sum = 0
	return matrix

def createTransitionsMatrixes():
	P_UD = np.zeros((16,16))
	P_S = np.zeros((16,16))
	P_LR = np.zeros((16,16))

	for i in range(0, 16):
		partida_lobo = X[i][0]
		partida_coelho = X[i][1]
		for j in range(0, 16):
			destino_coelho = X[j][1]
			destino_lobo = X[j][0]
			# Tendo em conta apenas os movimentos Stay do Lobo
			P_S[i][j] = P_lobo_s[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]
			# Tendo em conta apenas os movimentos Right e Left do Lobo
			P_LR[i][j] = P_lobo_rl[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]
			# Tendo em conta apenas os movimentos Up e Down do Lobo
			P_UD[i][j] = P_lobo_ud[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]

	return (P_UD, P_LR, P_S)

X = np.array([[0, 0], [0, 1], [0, 2], [0, 3],
    		  [1, 0], [1, 1], [1, 2], [1, 3], 
     		  [2, 0], [2, 1], [2, 2], [2, 3], 
     		  [3, 0], [3, 1], [3, 2], [3, 3]])

A = ('L', 'R', 'U', 'D', 'S')

P_coelho = np.array([[0.6, 0.2, 0.2, 0.0], 
					 [0.2, 0.6, 0.0, 0.2], 
					 [0.2, 0.0, 0.6, 0.2], 
					 [0.0, 0.2, 0.2, 0.6]])

P_lobo_rl = np.array([[0.2, 0.8, 0.0, 0.0], 
		     		  [0.8, 0.2, 0.0, 0.0], 
		     		  [0.0, 0.0, 0.2, 0.8], 
		     		  [0.0, 0.0, 0.8, 0.2]])
 
P_lobo_ud = np.array([[0.2, 0.0, 0.8, 0.0], 
			 		  [0.0, 0.2, 0.0, 0.8], 
		     		  [0.8, 0.0, 0.2, 0.0], 
		     		  [0.0, 0.8, 0.0, 0.2]])

P_lobo_s = np.array([[1.0, 0.0, 0.0, 0.0], 
					 [0.0, 1.0, 0.0, 0.0], 
		    		 [0.0, 0.0, 1.0, 0.0], 
		    	  	 [0.0, 0.0, 0.0, 1.0]])

P_UD, P_LR, P_S =  createTransitionsMatrixes()
labels = ["00", "01", "02", "03", "10", "11", "12", "13", "20", "21", "22", "23", "30", "31", "32", "33"]
print (DataFrame(P_UD, index=labels, columns=labels))
print (DataFrame(P_LR, index=labels, columns=labels))
print (DataFrame(P_S, index=labels, columns=labels))

Policy = np.array([0.0, 0.0, 1.0, 0.0, 0.0]) #isto não é policy nenhuma...

#--------------------- possivel tabela de custos --------------------------------

C = np.array([[1.0,  1.0,  1.0,   1.0,  0.0], #(0,0)
			  [0.0,  0.0,  1.0,   1.0,  1.0], #(0,1)
			  [1.0,  1.0,  0.0,   0.0,  1.0], #(0,2)
			  [1.0,  1.0,  1.0,   1.0,  1.0], #(0,3)

			  [0.0,  0.0,  1.0,   1.0,  1.0], #(1,0)
			  [1.0,  1.0,  1.0,   1.0,  0.0], #(1,1)
			  [1.0,  1.0,  1.0,   1.0,  1.0], #(1,2)
			  [1.0,  1.0,  0.0,   0.0,  1.0], #(1,3)

			  [1.0,  1.0,  0.0,   0.0,  1.0], #(2,0)
			  [1.0,  1.0,  1.0,   1.0,  1.0], #(2,1)
			  [1.0,  1.0,  1.0,   1.0,  0.0], #(2,2)
			  [0.0,  0.0,  1.0,   1.0,  1.0], #(2,3)

			  [1.0,  1.0,  1.0,   1.0,  1.0], #(3,0)
		 	  [1.0,  1.0,  0.0,   0.0,  1.0], #(3,1)
			  [0.0,  0.0,  1.0,   1.0,  1.0], #(3,2)
			  [1.0,  1.0,  1.0,   1.0,  0.0]]) #(3,3)

identityMatrix = np.identity(16)
gama = 0.99

print (DataFrame(C, index=labels, columns=['L', 'R', 'U', 'D', 'S']))

cost_policy_up = C[:,2]  #(16*1)

inverse = np.linalg.inv(identityMatrix-(gama*P_UD)) #(16*16) - gama*(16*16) = (16*16)
J = np.dot(inverse, cost_policy_up)
print (J)


