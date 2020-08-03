
# calculate the influence vector for a 
# citation network to determine eigenfactor scores

import numpy as np
import sys

def main():

	# —————————————————————————————————————
	# STEP 1: Load the data/create matrix
	# —————————————————————————————————————

	with open('citations_small.txt', 'r') as file:

		# please put the total number of articles as the first line of the file

		try:
			n = int(file.readline())
		except:
			print('Please type the total number of articles as the top line of the file')
			sys.exit(1)
		Z = np.array([0]*n**2).reshape(n,n)

		# read through each line of the file one by one, create adjacency matrix

		for line in file:
			if ('#i' in line):
				print()
				j = int(line[len('#index'):].strip('\n'))
				print(j, end=': ')
			if ('#%' in line):
				i = int(line[len('#%'):].strip('\n'))
				print(i, end=' ')
				Z[i,j] += 1


		# column labels indicate journals, row labels indicate references
		# element i,j is the number of times journal j cites i (arrows j->i)

		print('\n')
		print(Z)

		# ——————————————————————————————————
		# STEP 2: Modify adjacency matrix
		# ——————————————————————————————————

		# make the diagonal a row of zeros (eliminate self-citations)
		Z = Z - np.multiply(np.identity(n), Z)

		# normalize columns, divide by sum
		Zn = Z.sum(axis=0)
		H = np.true_divide(Z, Zn, where = (Zn != 0))
		H[np.isnan(H)] = 0

		# find dangling nodes, create a vector d to record them

		dangling_nodes = np.where(~H.any(axis=0))[0]
		d = np.array([0]*n)
		for i in range(len(dangling_nodes)):
			d[dangling_nodes[i]] = 1

		# ——————————————————————————————————
		# STEP 3: Initialize important values
		# ——————————————————————————————————

		alpha = 0.85 # why 0.85? this seems arbitrary to me
		epsilon = 0.00001

		# let A_tot be the total number of articles in all journals
		# in this example, A_tot = 3 + 2 + 5 + 1 + 2 + 1
		A_tot = n

		# a is a normalized column vector with the number of articles/journal
		a = np.array([1]*n).reshape(n,1)
		a = a / A_tot

		# calculate transition matrix P
		# TODO

		# initialize start vector/dummy vector to pass first while loop

		pi_k1 = 1/n * np.array([1]*n)
		pi_k = pi_k1 + 10

		# these are backwards because they get flipped in the algorithm below

		# ——————————————————————————————————
		# STEP 4: Calculate influence vector pi_i
		# ——————————————————————————————————

		# this algorithm should converge to the leading eigenvector of P
		# count iterations, out of curiosity

		iterations = 0
		while (abs(pi_k - pi_k1).all() > epsilon):
		    pi_k = pi_k1
		    pi_k1 = (alpha*H@pi_k).reshape(n,1) + (alpha*d@pi_k + (1-alpha)) * a
		    iterations += 1

		pi = pi_k1

		print('\niterations = ', str(iterations))

		print('\npi = \n\n', str(pi), '\n———————————————\n')

		# —————————————————————————————————————————————————————————

		# We now have the stationary vector and can calculate a variety of scores

		# ———

		# Eigenfactor score

		EF = 100 * H@pi / (H@pi).sum()

		print('eigenfactor scores = \n\n', str(EF), '\n———————————————\n')


		# ———

		# Article Influence Score

		AI = 0.01 * np.true_divide(EF, a);

		print('article influence scores = \n\n', str(AI), '\n———————————————\n')


main()












