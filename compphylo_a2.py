# -*- coding: utf-8 -*-
"""
ZacCarver
02-06-17
CompPhylo assignment 2
"""
#import timeit as timeit
import random
import numpy as np

def factori(prod, mn, mx):
	for i in range(mn,mx+1):#for i in range(mn,mx):
		prod = prod*i
	return prod#return prod*mx

#def coef_1(prod, f, mn, mx, k):
    #coef_1 = f/(factori(prod,1,(mx-mn))*k)
    #return coef_1
'''
Ok, so for whatever reason the alternative binomial function was not cooperating.
I believe that a range() should be set to then multiply consecutively in decreasing order?
But this resembles the following function rather closely....
'''  

def coef_2(mn,mx,k):
	#stackoverflow posting help http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
	coef_2 =1#start off the values in a given range at 1
	for n in range(mx, mx-mn, -1):
		coef_2 = coef_2*n#multiply each value in the range to the previous and return
	return coef_2/k#divide the end product by factorial of the mn to obtain the coefficient value
	
def prob_knp(mn, mx, k, p):
    k = int(k)#because the binomial function cannot divide an integer by a float, convert k to integer
    P = coef_2(mn,mx,k)*pow(p,mn)*pow((1-p),(mx-mn))#calculate pmf to return the probability
    return P

def smpl_rand(l, px):
    # posting help: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch04s22.html
    x = random.uniform(0,1)#uniform is for floats
    prob_tot = 0.0
    for item, prob_indi in zip(l, px):#for each item and its probability 
        prob_tot += prob_indi
        if x < prob_tot:
            break
    return item

def ML_hill(diff, mn, mx, k, p):
    '''
    ***remembering while loops....http://stackoverflow.com/questions/1662161/is-there-a-do-until-in-python
    With the inputs for the pmf function above (prob_knp), a lower parameter and an upper parameter are set as a sliding window for consecutive pvalues climbing
    up a normal curve to the maximum likelihood of m.
    '''
    pCurr = p
    #likeCurr = prob_knp(mn, mx, k, pCurr)
    #like_R = prob_knp(mn, mx, k, pRight)
    #like_L = prob_knp(mn, mx, k, pLeft)
    #print(likeCurr, like_R, like_L, pCurr, pRight, pLeft)
    while diff > 0.000001:
        pUp = pCurr + diff#set the upper parameter 0.1 above the current probability
        pDwn = pCurr - diff#set the lower parameter 0.1 below the current probability
        like_pCurr = prob_knp(mn, mx, k, pCurr)#get the current likelihood of the probability (pmf)
        like_pUp = prob_knp(mn, mx, k, pUp)#get the upper likelihood of the upper parameter
        like_pDwn = prob_knp(mn, mx, k, pDwn)#get the lower likelihood of the lower parameter
        if like_pUp > like_pCurr:
            pCurr = pUp
            #pUp = pCurr + diff #variables in this instance have to be outside of loop
            continue #continues to the next statement
        if like_pDwn > like_pCurr:
            pCurr = pDwn
            #pDwn = pCurr - diff
            continue
        if like_pUp < like_pCurr or like_pDwn < like_pCurr:#once the 'max' has been overshot...
            diff = diff*0.5#change the 'window' and reverse direction
            continue
        if diff < 0.0001:#loop until this threshold is passed, break out of loop and return the desired likelihood.. 
            break
    return like_pCurr        
    
def sim_likeRatio(diff,mn, mx, p, pmf):
    '''
    Simulates 100 trials of k and calculates the likelihood of each value compared to the true probability such that LR = ((p')^k(1-p')^n-k)/((p)^k(1-p)^n-k)
    with these ratios, the cutoff for the greatest 5% is then returned by sorting the list of 100 LRs.
    '''
    #mn = 1
    #mx = 6
    #http://stackoverflow.com/questions/22071987/generate-random-array-of-floats-between-a-range
    kvals = [random.randrange(mn,mx) for x in range(100)]#random.uniform give random floats and random.randrange gives integral values.
    #print("kvals =\n", kvals)
    likevals = []
    like_ratios = []
    for k in kvals:
        likevals.append(ML_hill(diff, mn, mx, k, pmf))
    print("likevals =\n", likevals,"\n\n")
    for likes in likevals:
        #print("k=\n",k)
        #print("likes=\n",likes)
        r = likes/pmf
        like_ratios.append(r)
    #print("ratios =\n", like_ratios)
    #sort the list to find the 5% of LR values considered too large...
    like_ratios = sorted(like_ratios, key=float)
    print("ratios =\n", like_ratios,"\n\n")
    LRcutoff = like_ratios[95]
    print("Probability of this Likelihood Ratio is <=5% :\n",LRcutoff)
        
    #print("pvals =\n", pvals)
        #for kval in kvals:
    		
def main():
    mn = 1
    mx = 6
    #prod = 1
    #f = factori(prod, mn, mx)
    #f_mn = factori(prod, 1, mn)
    #print(f)
    k = factori(1, 1, mn)
    #n = factori(1, 1, mx)
    print("k =", k,"\n\n")
    p = 0.2
    l = [1,2,3,4]
    px = [0.2, 0.3, 0.1, 0.4]
    diff = 0.1
    #print(coef_1(prod, f, mn, mx, k))
    print(mx, "choose", mn, "=", coef_2(mn,mx,k),"\n\n")
    pmf = prob_knp(mn, mx, k, p)
    print("pmf=\n", pmf,"\n\n")
    print(smpl_rand(l, px))
    ML = ML_hill(diff, mn, mx, k, p)
    print("Maximum Likelihood=\n",ML,"\n\n")
    sim_likeRatio(diff,mn, mx, p, pmf)
    
if __name__ == '__main__':
	main()

