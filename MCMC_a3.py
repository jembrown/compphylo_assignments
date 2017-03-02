# -*- coding: utf-8 -*-

"""
ZacCarver
02-06-17
CompPhylo assignment 3
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, uniform


def like(k, n, p, testPrior=False):
	'''Defined function to find likelihood if p>0 & p<1. To test if the script is behaving properly change the testPrior=True where the prior will always be one. '''
	if testPrior:
		return 1
	if p < 0:
		return 0
	elif p > 1:
		return 0
	else:
		lk = binom.pmf(k,n,p) #if the parameters from above are satisfied the probability mass (likelihood) is returned for the given k, n & p
		return lk

def prior(p):
	'''Defined function to find the probability density with a uniform distribution between [0,1] and a mean of 0.5'''
	prr = uniform.pdf(p)
	return prr

def posterior_UN(prr, lk):
	'''an unnormalized posterior density, prior(or pdf) * likelihood(or pmf)'''
	posterior = prr*lk
	return posterior

def draw_param(n, p):
	'''draws one random number based on the number of trials with the probability of each trial to return a new parameter k(or state). scipy.org'''
	newk = np.random.binomial(n, p, 1)
	#newp = norm.rvs(size=1,loc=p,scale=1)
	return newk[0]#because np returns an array, the element within the array is isolated and returned 
	#return newp

def acc_rej(curr_post, new_post):
	'''function will accept or reject a 'move' based on the current position/posterior value'''
    r = new_post/curr_post
    if r > 1:
    	post = new_post #instead of comparing and moving on the state, here the chain moves on the posterior (this is what I had before changing the chain to look at the states...)
        #state = new_param
        return post
        #return state
    else:
        rand_r = random.uniform(0,1)#pull from a continuous distribution between 0 & 1
        if rand_r < r:#if the randome value is less than r, accept the proposed parameter as the current state. 
        	post = new_post
            #state= new_param
            return post
            #return state
        else:
        	post = curr_post
            #state = curr_param
            return post
            #return state

def plots(param_vals, likelihoods, posteriors):
	'''Histograms of the parameter values (priors), likelihoods and posteriors.'''
	plt.hist(param_vals)
	plt.title("Priors")
	plt.xlabel("Priors")
	plt.ylabel("Frequency")
	plt.show()

	plt.hist(likelihoods)
	plt.title("Likelihoods")
	plt.xlabel("Priors")
	plt.ylabel("Frequency")
	plt.show()

	plt.hist(posteriors)
	plt.title("Posteriors")
	plt.xlabel("Priors")
	plt.ylabel("Frequency")
	plt.show()


def MCMC():
	#define some binomial dataset, coinflips
	flips = ["H","H","T","H","T"]
	k = sum([1 for fl in flips if fl == "T"])
	n = len(flips)
	p = 0.2
	lk = like(k, n, p)
	prr = prior(p)
	curr_param = draw_param(n, p)
	curr_post = posterior_UN(prr, lk)
	param_vals = []#define a list to hold the chained parameter values from the Markov chain.
    likelihoods =  []#define a list to hold the found likelihoods
    posteriors = []#define a list to hold the posteriors 
    '''VVVV chain VVVV'''
	for val in range(100):#go through an x number of replicates, here 100
		new_param = draw_param(n, p)#each iteration draw a new and random parameter in n trials with a probability of p
	    #normp = np.random.triangular(0,1,1)
	    likelihoods.append(like(new_param, n, p))
		new_post = posterior_UN(prr, like(new_param, n, p))
		posteriors.append(posterior_UN(prr, like(new_param, n, p)))
		param_vals.append(acc_rej(curr_post, new_post))
	print('yes', param_vals)
	plots(param_vals, likelihoods, posteriors)#now plot the histograms.
	

if __name__ == '__main__':
	MCMC()


'''
example of thought process...
iter = []
p = 0.1
iter.append(p)
for _ in ngen:
	pnew = propose(p)
	r= calcRatio(pnew, p)
	p = sample([pnew,p],[r,1-r])
	iter.append(p)
'''