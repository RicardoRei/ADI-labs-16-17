import numpy as np

def createTransictionsMatrix():
	P = np.zeros((16,16))

	for i in range(0, 16):
		linha_lobo = X[i][0]
		linha_coelho = X[i][1]
		for j in range(0, 16):

			coluna_coelho = X[j][1]
			coluna_lobo = X[j][0]

			if abs((coluna_lobo - linha_lobo)) == 0 : #diferenca de 0 implica stay
				P[i][j] = P_lobo_s[linha_lobo][coluna_lobo] * P_coelho[linha_coelho][coluna_coelho]

			elif abs((coluna_lobo - linha_lobo)) == 1: #diferenca de 1 implica deslocamento lateral
				P[i][j] = P_lobo_rl[linha_lobo][coluna_lobo] * P_coelho[linha_coelho][coluna_coelho]

			elif abs((coluna_lobo - linha_lobo)) == 2: #diferenca de 2 implica deslocamento vertical
				P[i][j] = P_lobo_ud[linha_lobo][coluna_lobo] * P_coelho[linha_coelho][coluna_coelho]

			print("| %d%d-%d%d: %.3f " % (linha_lobo, linha_coelho, coluna_lobo, coluna_coelho, P[i][j]), end='')
		print('')
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

P = createTransictionsMatrix()

Policy = np.array([0.0, 0.0, 0.0, 1.0, 0.0])
#--------------------- possivel tabela de custos --------------------------------

C = [[0.0,  0.0,  0.0,   0.0,  1.0], #(0,0)
	 [0.5,  0.5,  0.0,   0.0,  0.0], #(0,1)
	 [0,    0,    0.5,   0.5,  0.0], #(0,2)
	 [0.25, 0.25, 0.25,  0.25, 0.0], #(0,3)
	 
	 [0.5,  0.5,  0.0,   0.0,  0.0], #(1,0)
	 [0.0,  0.0,  0.0,   0.0,  1.0], #(1,1)
	 [0.25, 0.25, 0.25,  0.25, 0.0], #(1,2)
	 [0.0,  0.0,  0.5,   0.5,  0.0], #(1,3)

	 [0.0,  0.0,  0.5,   0.5,  0.0], #(2,0)
	 [0.25, 0.25, 0.25,  0.25, 0.0], #(2,1)
	 [0.0,  0.0,  0.0,   0.0,  1.0], #(2,2)
	 [0.5,  0.5,  0.0,   0.0,  0.0], #(2,3)

	 [0.25, 0.25, 0.25,  0.25, 0.0], #(3,0)
	 [0.0,  0.0,  0.5,   0.5,  0.0], #(3,1)
	 [0.5,  0.5,  0.0,   0.0,  0.0], #(3,2)
	 [0.0,  0.0,  0.0,   0.0,  1.0]] #(3,3) 
