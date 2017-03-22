import numpy as np

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

def createTransitionsMatrix():
	P = np.zeros((16,16))

	for i in range(0, 16):
		partida_lobo = X[i][0]
		partida_coelho = X[i][1]
		for j in range(0, 16):

			destino_coelho = X[j][1]
			destino_lobo = X[j][0]

			if abs((destino_lobo - partida_lobo)) == 0 : #diferenca de 0 implica stay
				P[i][j] = P_lobo_s[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]

			elif abs((destino_lobo - partida_lobo)) == 1: #diferenca de 1 implica deslocamento lateral
				P[i][j] = P_lobo_rl[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]

			elif abs((destino_lobo - partida_lobo)) == 2: #diferenca de 2 implica deslocamento vertical
				P[i][j] = P_lobo_ud[partida_lobo][destino_lobo] * P_coelho[partida_coelho][destino_coelho]

			#print("| %d%d-%d%d: %.3f " % (partida_lobo, partida_coelho, destino_lobo, destino_coelho, P[i][j]), end='')
		#print('')
	return P

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
		     		  [0.0, 0.2, 0.8, 0.2]])
 
P_lobo_ud = np.array([[0.2, 0.0, 0.8, 0.0], 
			 		  [0.0, 0.2, 0.0, 0.8], 
		     		  [0.8, 0.0, 0.2, 0.0], 
		     		  [0.0, 0.8, 0.0, 0.2]])

P_lobo_s = np.array([[1.0, 0.0, 0.0, 0.0], 
					 [0.0, 1.0, 0.0, 0.0], 
		    		 [0.0, 0.0, 1.0, 0.0], 
		    	  	 [0.0, 0.0, 0.0, 1.0]])

P = createTransitionsMatrix()

Policy = np.array([0.0, 0.0, 1.0, 0.0, 0.0])

P_normalized = normalizeMatrix(P)

#--------------------- possivel tabela de custos --------------------------------

C = [[1.0,  1.0,  1.0,   1.0,  0.0], #(0,0)
	 [0.0,  0.0,  2.0,   2.0,  1.0], #(0,1)
	 [2.0,  2.0,  0.0,   0.0,  1.0], #(0,2)
	 [1.0,  1.0,  1.0,   1.0,  2.0], #(0,3)
	 
	 [0.0,  0.0,  2.0,   2.0,  1.0], #(1,0)
	 [1.0,  1.0,  1.0,   1.0,  0.0], #(1,1)
	 [1.0,  1.0,  1.0,   1.0,  2.0], #(1,2)
	 [2.0,  2.0,  0.0,   0.0,  1.0], #(1,3)

	 [2.0,  2.0,  0.0,   0.0,  1.0], #(2,0)
	 [1.0,  1.0,  1.0,   1.0,  2.0], #(2,1)
	 [1.0,  1.0,  1.0,   1.0,  0.0], #(2,2)
	 [0.0,  0.0,  2.0,   2.0,  1.0], #(2,3)

	 [1.0,  1.0,  1.0,   1.0,  2.0], #(3,0)
	 [2.0,  2.0,  0.0,   0.0,  1.0], #(3,1)
	 [0.0,  0.0,  2.0,   2.0,  1.0], #(3,2)
	 [1.0,  1.0,  1.0,   1.0,  0.0]] #(3,3)

C_normalized = normalizeMatrix(C)

print (C_normalized)
print (P_normalized)
