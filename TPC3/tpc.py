X={Carta paus,Carta ouros};
A={Guess paus,Guess ouros,Espreitar};
Z={Ver paus, Ver ouros};

P_guessPaus = P_guessOuros = [{0.5,0.5}
							,{0.5,0.5}]	

P_espreitar=	[{1,0}
				,{0,1}]



O_espreitar= 	[{0.9,0.1},
				{0.1,0.9}]

O_guessPaus = O_guessOuros	=	[{0.5,0.5},
								{0.5,0.5}]

Cost = [{1,-1,0.1},
		{-1,1,0.1}]

alpha_0 = [{0.7,0.3}];
alpha_1_chapeu = alpha_0* P_espreitar=alpha_0

alpha_1 = alpha_1_chapeu * [{0.1,0},{0,0.9}]

