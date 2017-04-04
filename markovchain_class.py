#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:49:38 2017

@author: piplup
"""
import random
from numpy.linalg import matrix_power


class mchain(object):
    def __init__(self,states=[], matrix=[], steps=10, chains=10):
        self.matrix = matrix
        self.states = states
        self.steps = steps
        self.chains = chains
        self.sample = []
        self.samplelist = []
    
    
    def run(self):
        '''initializes the class by passing the index of the current state to the draw fxn to build a chain''' 
        for _ in range(0,self.chains):
            self.sample = []
            for _ in range(0,self.steps):
                #print(self.sampled)
                #self.matrix[self.states.index(state)]
                #curr_index = states.index(curr_state)
                #print(self.states)
                state = self.draw(self.states, self.matrix)
                self.sample.append(state)
            self.samplelist.append(self.sample)
        return self.samplelist
    
    
    def draw(self, states, matrix):
        '''draws the next state based on the initial state and its probability from the matrix'''
        x = random.uniform(0,1)#uniform is for floats
        #print(x)
        prob_tot = 0.0
        for state, mat_prob in zip(states, matrix):#for each item and its probability 
            #print(state)
            curr_index = states.index(state)
            #print(curr_index)
            prob_tot += mat_prob[curr_index]
            #print(state, prob_tot)
            if x < prob_tot:
                break#if condition is met, break from loop
        return state 

        
    def frequencies(self, st):
        '''summarized frequency for a given state across X chains(replicates)'''
        freqs = {}
        for chain in self.samplelist:
            for s in chain:
                if s in freqs.keys():
                    freqs[s] +=1
                else:
                    state = s
                    value = 1
                    freqs[state] = value
        if st[0] in freqs:
            f = freqs[st[0]]/self.chains
            print("\nTotal frequency of",st,"is",f,"%","across",self.chains,"chain simulations\n\n")
            
            
    def forward_prob(self,c):
        '''Calculated probability for a given chain going forward by iteratively multiplying each state's probability'''
        prob = 1.0
        chain = self.samplelist[c]
        for st in chain:#iterativly multiply each state's probability 
            #print(st)
            for state, mat_prob in zip(self.states,self.matrix):
                curr_index = states.index(state)
                prob *= mat_prob[curr_index]
                if state == st:
                    break
        print("forward probability for selected chain:\n",prob,"\n\n")
    
    
    def reverse_prob(self,c):
        '''Calculated probability for a given chain going backward by iteratively multiplying each state's probability'''
        prob = 1.0
        chain = self.samplelist[c]
        #used the reverse function to reverse the order of each state in chain.
        for st in reversed(chain):#iteratively multiply each state's probability
            #print(st)
            for state, mat_prob in zip(self.states,self.matrix):
                curr_index = states.index(state)
                prob *= mat_prob[curr_index]
                if state == st:
                    break
        print("reverse probability for selected chain:\n",prob,"\n\n")
                #if st == state:
                    #curr_index = self.states.index(st)
                    #print(st, curr_index)
                    #prob *= mat_prob[curr_index]
                    #print(mat_prob)
            #print(curr_index)
                    #prob *= self.matrix[curr_index]
        #print(prob)
    
    
    def marginal_prob(self, c):
        '''unsure if this marginalizes properly, but here the matrix is raised to the number of steps in the chain and is used to assign probabilities to each state. The total probability is then found by iteratively multiplying each state's probability'''
        prob = 1.0
        #need to set the default decimal places kept higher
        marg_mat = matrix_power(self.matrix, self.steps)
        #print(marg_mat)
        chain = self.samplelist[c]
        for st in chain:#iteratively multiply each state's probability
            for state, mat_prob in zip(self.states, marg_mat):
                curr_index = states.index(state)
                prob *= mat_prob[curr_index]
                if state == st:
                    break
        print("marginalized probability for selected chain:\n",prob)
        
        
###############################################################################    
states = ['r','s','sn']
#print(states)
st = ['s']
c = 0
#end = []
matrix = [[0.6,0.3,0.1],[0.3,0.1,0.6],[0.1,0.6,0.3]]

test = mchain(states, matrix)
test.run()
test.frequencies(st)
test.forward_prob(c)
test.reverse_prob(c)
test.marginal_prob(c)

