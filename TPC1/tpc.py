import numpy as np
from numpy import linalg as ln

""" 
Board Postion, state translation:

Go = 0
Vermont Avenue = 1
Jail = 2
Virginia Avenue = 3
Free Parking = 4
Marvin Gardens = 5
Go to Jail = 6
Pennsylvania Avenue = 7

"""

X = [ 0, 1, 2, 3, 4, 5, 6, 7 ]  #the set of all states possible

# Transition probability matrix
P = np.array([[0.0, 1/6, 1/6, 1/6, 1/6, 1/6, 1/6, 0.0], #0
			  [0.0, 0.0, 1/6, 1/6, 1/6, 1/6, 1/6, 1/6], #1
			  [1/6, 0.0, 0.0, 1/6, 1/6, 1/6, 1/6, 1/6], #2
			  [1/6, 1/6, 0.0, 0.0, 1/6, 1/6, 1/6, 1/6], #3
			  [1/6, 1/6, 1/6, 0.0, 0.0, 1/6, 1/6, 1/6], #4
			  [1/6, 1/6, 1/6, 1/6, 0.0, 0.0, 1/6, 1/6], #5
			  [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], #6
			  [1/6, 1/6, 1/6, 1/6, 1/6, 1/6, 0.0, 0.0]]) #7

M = (X, P) # Markov chain

s0 = np.array([1, 0, 0, 0, 0, 0, 0, 0]) #initial state

P3 = ln.matrix_power(P, 3)

res = np.dot(P3, s0)

print(res)


